import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes import router, user_router, ai_router, doctor_router

from settings import settings

import sqlite3

def create_connection():
 connection = sqlite3.connect("books.db")
 return connection

# Create an instance of the FastAPI class
app = FastAPI()
app.mount('/audios', StaticFiles(directory='audios'),'audios')
app.include_router(router)
app.include_router(user_router, prefix='/api/v1', tags=["user"])
app.include_router(ai_router, prefix='/api/v1', tags=["AI Voice"])
app.include_router(doctor_router, prefix='/api/v1', tags=["Doctor"])

origins = [
    "http://localhost:5173",
    "https://voice-chatbot-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )