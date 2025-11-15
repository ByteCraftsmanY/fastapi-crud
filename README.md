# FastAPI Task Management CRUD Service

## Setup

1. Clone the repo
2. Install uv
3. Navigate to repo directory
4. Run `uv venv` for venv setup
5. Run `uv sync` to install dependencies

## Running the Project

### If you already have a PostgreSQL database

Export URL in terminal before running the app:

```bash
export DATABASE_URL=postgresql+psycopg2://admin:admin123@localhost:5432/test
```

Then run the project:

```bash
uvicorn app.main:app
```

### Otherwise

Run docker-compose to start the app with database inside Docker:

```bash
docker-compose up -d --build
```

## Testing

Run the tests using pytest:

```bash
pytest test.py
```
