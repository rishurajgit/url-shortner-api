# URL Shortener API

A simple URL Shortener API built using FastAPI and PostgreSQL.

The API allows users to create shortened URLs and redirect users from a short code to the original URL.

## Features

- Create shortened URLs from long URLs
- Generate unique short codes
- Store URLs in PostgreSQL
- Redirect short URLs to their original URLs
- Validate URLs using Pydantic
- Return `404 Not Found` for invalid short codes

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Pydantic

## Project Structure

```text
url-shortner-api/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── short_code.py
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── requirements.txt
```

## Prerequisites

Make sure you have the following installed:

- Python
- Docker Desktop

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd url-shortner-api
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the environment file

Copy `.env.example` and rename it to `.env`.

The `.env` file should contain:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/url_shortener
BASE_URL=http://localhost:8000
```

### 5. Start PostgreSQL using Docker

```bash
docker compose up -d
```

Verify that the PostgreSQL container is running:

```bash
docker ps
```

## Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### POST `/shorten`

Creates a shortened URL.

#### Request

```json
{
  "url": "https://www.google.com"
}
```

#### Response

```json
{
  "short_code": "4gyAaV",
  "short_url": "http://localhost:8000/4gyAaV"
}
```

The API generates a unique short code and stores the original URL and short code in PostgreSQL.

---

### GET `/{short_code}`

Redirects the user to the original URL.

Example:

```text
http://localhost:8000/4gyAaV
```

If the short code exists, the API responds with:

```text
307 Temporary Redirect
```

and redirects the user to the original URL.

If the short code does not exist, the API returns:

```json
{
  "detail": "Short URL not found"
}
```

with a `404 Not Found` status.

## Database

PostgreSQL runs inside a Docker container.

To access the database:

```bash
docker exec -it url-shortener-db psql -U postgres -d url_shortener
```

To view stored URLs:

```sql
SELECT * FROM urls;
```

To exit PostgreSQL:

```text
\q
```

## API Flow

### POST `/shorten`

```text
Long URL
   ↓
Validate URL
   ↓
Generate unique short code
   ↓
Store in PostgreSQL
   ↓
Return shortened URL
```

### GET `/{short_code}`

```text
Short URL
   ↓
Find short code in PostgreSQL
   ↓
Retrieve original URL
   ↓
307 Temporary Redirect
   ↓
Original URL
```

## Environment Variables

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | PostgreSQL database connection URL |
| `BASE_URL` | Base URL used to generate shortened URLs |

## Stopping PostgreSQL

To stop the Docker container:

```bash
docker compose down
```


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Rishu Raj