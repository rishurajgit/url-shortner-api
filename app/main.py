from fastapi import FastAPI, Depends, HTTPException, status
from app.database import Base, engine, get_db
from app.models import URL
from sqlalchemy.orm import Session
from app.schemas import URLCreate, URLResponse
from app.short_code import generate_short_code
from fastapi.responses import RedirectResponse

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
    
@app.post(
    "/shorten",
    response_model=URLResponse,
    status_code=status.HTTP_201_CREATED,
)
def shorten_url(
    url_data: URLCreate,
    db: Session = Depends(get_db),
):
    short_code = generate_short_code()

    existing_url = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    while existing_url:
        short_code = generate_short_code()

        existing_url = db.query(URL).filter(
            URL.short_code == short_code
        ).first()

    new_url = URL(
        original_url=str(url_data.url),
        short_code=short_code,
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "short_code": new_url.short_code,
        "short_url": f"http://localhost:8000/{new_url.short_code}",
    }
    
@app.get("/{short_code}")
def redirect_to_url(
    short_code: str,
    db: Session = Depends(get_db),
):
    url = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        )

    return RedirectResponse(
        url=url.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )