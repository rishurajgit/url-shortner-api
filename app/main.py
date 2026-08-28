from fastapi import FastAPI
from app.database import Base, engine
from app.models import URL

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortener built with FastAPI.",
    version="1.0.0",
)

@app.get("/")
def health_check():
    return {
        "message": "URL Shortener API is running"
    }