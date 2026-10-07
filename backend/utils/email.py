# backend/utils/email.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

MAIL_EMAIL    = os.getenv('MAIL_EMAIL')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
FRONTEND_URL  = os.getenv('FRONTEND_URL', 'http://127.0.0.1:3000').rstrip('/')

def send_reset_email(to_email: str, reset_token: str, user_name: str):
    """
    Sends a password reset email to the user.

    Why we use Gmail SMTP:
    SMTP is the protocol for sending emails.
    Gmail provides a free SMTP server we can use
    to send emails directly from Python.
    """

    # The reset link — user clicks this to reset password
    reset_link = f"{FRONTEND_URL}/reset-password.html?token={reset_token}"

    # Build the email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Reset Your Legal Aid Provider Password'
    msg['From']    = MAIL_EMAIL
    msg['To']      = to_email

    # Plain text version
    text = f"""
Hi {user_name},

You requested a password reset for your Legal Aid Provider account.

Click the link below to reset your password:
{reset_link}

This link expires in 15 minutes.

If you did not request this, please ignore this email.

Legal Aid Provider Team
    """

    # HTML version — looks nicer in email client
    html = f"""
    <html>
    <body style="font-family: Inter, sans-serif; background: #070b14; color: #f0f4ff; padding: 40px;">
        <div style="max-width: 500px; margin: 0 auto; background: #101828; border: 1px solid rgba(232,184,75,0.25); border-radius: 16px; padding: 40px;">
            <div style="text-align: center; margin-bottom: 28px;">
                <span style="font-size: 36px;">⚖️</span>
                <h1 style="font-family: Georgia, serif; color: #e8b84b; margin-top: 10px;">Legal Aid Provider</h1>
            </div>
            <h2 style="color: #f0f4ff; margin-bottom: 16px;">Reset Your Password</h2>
            <p style="color: #6b7a99; line-height: 1.7;">Hi {user_name},</p>
            <p style="color: #6b7a99; line-height: 1.7;">
                You requested a password reset. Click the button below to create a new password.
                This link expires in <strong style="color: #e8b84b;">15 minutes</strong>.
            </p>
            <div style="text-align: center; margin: 32px 0;">
                <a href="{reset_link}"
                   style="background: linear-gradient(135deg, #e8b84b, #f5d07a);
                          color: #070b14; padding: 14px 32px; border-radius: 10px;
                          text-decoration: none; font-weight: 700; font-size: 15px;">
                    Reset Password
                </a>
            </div>
            <p style="color: #6b7a99; font-size: 13px; line-height: 1.7;">
                If you did not request this, please ignore this email.
                Your password will not change.
            </p>
            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 24px 0;"/>
            <p style="color: #6b7a99; font-size: 12px; text-align: center;">
                Legal Aid Provider · For informational purposes only
            </p>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html,  'html'))

    try:
        # Connect to Gmail SMTP server and send
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MAIL_EMAIL, MAIL_PASSWORD)
            server.sendmail(MAIL_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False