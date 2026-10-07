from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
import secrets
from dotenv import load_dotenv
from pathlib import Path
from database import get_db
from models.user import User
from utils.email import send_reset_email

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

router       = APIRouter()
pwd_ctx      = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY   = os.getenv('SECRET_KEY', 'changeme')
ALGORITHM    = 'HS256'
TOKEN_EXPIRE = 60 * 24 * 7

def hash_password(p):      return pwd_ctx.hash(p)
def verify_password(p, h): return pwd_ctx.verify(p, h)

def create_token(user_id, email):
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE)
    return jwt.encode(
        {'sub': str(user_id), 'email': email, 'exp': expire},
        SECRET_KEY, algorithm=ALGORITHM
    )

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid or expired token')

# ── Request schemas ──
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


# ── Signup ──
@router.post('/signup')
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail='Email already registered')
    user = User(
        name     = data.name,
        email    = data.email,
        password = hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        'token': create_token(user.id, user.email),
        'name':  user.name,
        'email': user.email
    }


# ── Login ──
@router.post('/login')
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid email or password')
    return {
        'token': create_token(user.id, user.email),
        'name':  user.name,
        'email': user.email
    }


# ── Forgot password ──
@router.post('/forgot-password')
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    What this does:
    1. Checks if email exists in database
    2. Generates a random secure token
    3. Saves token + expiry to database
    4. Sends email with reset link

    Why we don't say "email not found":
    Security reason — if we say "email not found",
    attackers can use this to find out which emails
    are registered. So we always return the same
    success message regardless.
    """
    user = db.query(User).filter(User.email == data.email).first()

    if user:
        # Generate a secure random token — 32 random bytes = 64 character hex string
        reset_token = secrets.token_hex(32)

        # Token expires in 15 minutes
        expiry = datetime.utcnow() + timedelta(minutes=15)

        # Save token to database
        user.reset_token        = reset_token
        user.reset_token_expiry = expiry
        db.commit()

        # Send reset email
        send_reset_email(user.email, reset_token, user.name)

    # Always return same message — security best practice
    return {'message': 'If this email is registered, a reset link has been sent.'}


# ── Reset password ──
@router.post('/reset-password')
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    What this does:
    1. Finds user by reset token
    2. Checks token has not expired
    3. Updates password with new bcrypt hash
    4. Clears the reset token so it cannot be used again
    """

    # Find user by token
    user = db.query(User).filter(User.reset_token == data.token).first()

    # Token not found
    if not user:
        raise HTTPException(status_code=400, detail='Invalid or expired reset link')

    # Token expired
    if datetime.utcnow() > user.reset_token_expiry:
        raise HTTPException(status_code=400, detail='Reset link has expired. Please request a new one.')

    # Validate new password length
    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail='Password must be at least 6 characters')

    # Update password with new hash
    user.password           = hash_password(data.new_password)

    # Clear the token — cannot be used again
    user.reset_token        = None
    user.reset_token_expiry = None

    db.commit()

    return {'message': 'Password reset successfully. You can now login with your new password.'}