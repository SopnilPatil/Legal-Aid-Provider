from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models.user
import models.conversation
from routes.chat    import router as chat_router
from routes.auth    import router as auth_router
from routes.history import router as history_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Legal Aid Provider API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows ALL origins — safe for local development
    allow_credentials=False,  # must be False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,    prefix='/api/auth')
app.include_router(chat_router,    prefix='/api')
app.include_router(history_router, prefix='/api/history')

@app.get('/')
def root():
    return {'status': 'Legal Aid Provider backend is running'}