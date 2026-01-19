import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routes.tasks import router as tasks_router
from routes.auth import router as auth_router
from routes.auth_google import router as google_auth_router
from config.database import Base, engine

# 🔹 Load environment variables FIRST
load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="API for managing tasks.",
)

# 🔐 REQUIRED for OAuth (Authlib)
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
if not SESSION_SECRET_KEY:
    raise RuntimeError("SESSION_SECRET_KEY is not set")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    same_site="lax",
    https_only=False,  # set True in production (HTTPS)
)

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 Routers
app.include_router(auth_router)
app.include_router(google_auth_router)
app.include_router(tasks_router)
