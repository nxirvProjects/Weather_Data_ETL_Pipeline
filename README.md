# Weather Data Pipeline

An ELT pipeline that fetches weather data from the Weatherstack API, loads it into PostgreSQL, and uses Apache Airflow to run it automatically on a schedule. dbt transformations will be added next.

## Pipeline Overview

```
Weatherstack API  →  PostgreSQL (raw)  →  Airflow (scheduled)  →  dbt (transforms)
    Extract              Load               Orchestrate             Transform
```

## Project Structure

```
weather-data-project/
├── api-request/
│   ├── api_request.py       # fetches weather data from Weatherstack API
│   └── insert_records.py    # connects to Postgres and inserts the data
├── airflow/
│   └── dags/
│       └── orchestrator.py  # Airflow DAG that runs the pipeline on a schedule
├── postgres/
│   └── airflow_init.sql     # sets up the airflow database on first run
├── docker-compose.yaml      # defines the Postgres and Airflow containers
├── .env                     # secrets (API key, DB credentials) — not committed to git
└── .gitignore
```

## Setup

### 1. Prerequisites
- Docker Desktop installed and running
- A Weatherstack API key (sign up at weatherstack.com)

### 2. Create your .env file
Create a `.env` file in the project root with the following:
```
WEATHER_API_KEY=your_api_key_here

POSTGRES_DB=db
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
```

### 3. Start the containers
```bash
docker compose up
```

This starts two containers:
- **postgres_container** — the PostgreSQL database (accessible on port 5000 from your machine)
- **airflow_container** — Apache Airflow (accessible at http://localhost:8000)

### 4. Open the Airflow UI
Go to http://localhost:8000 in your browser. The DAG `weather-api-orchestrator` will appear and run automatically every 5 minutes.

---

## Commands Reference

### Docker

| Command | What it does |
|---|---|
| `docker compose up` | Start all containers |
| `docker compose down` | Stop and remove containers (keeps data) |
| `docker compose down -v` | Stop and remove containers AND delete all data (fresh start) |

### Entering the PostgreSQL database

```bash
docker compose exec db psql -U db_user -d db
```

| Part | What it means |
|---|---|
| `docker compose exec db` | Run a command inside the `db` container |
| `psql` | Open the PostgreSQL command line |
| `-U db_user` | Log in as this user |
| `-d db` | Connect to this database |

### psql commands (run these inside the psql terminal)

| Command | What it does |
|---|---|
| `\dn` | List all schemas |
| `\dt` | List all tables in the current schema |
| `\dt dev.*` | List all tables in the `dev` schema |
| `\d dev.raw_weather_data` | Show the columns and structure of the weather table |
| `\q` | Quit the psql terminal |

### Useful SQL queries

```sql
-- Check how many rows have been inserted
SELECT COUNT(*) FROM dev.raw_weather_data;

-- View the most recent 10 rows
SELECT * FROM dev.raw_weather_data ORDER BY inserted_at DESC LIMIT 10;
```

### Git

| Command | What it does |
|---|---|
| `git add filename.py` | Stage a specific file |
| `git add .` | Stage all changed files |
| `git commit -m "message"` | Commit staged changes |
| `git push` | Push commits to GitHub |
| `git status` | See what files have changed |
| `git diff` | See exact line changes |

---

## Notes

- `mock_fetch_data()` in `api_request.py` returns hardcoded data so you can test without hitting the real API and burning through rate limits. Switch to `fetch_data()` when ready for real data.
- Secrets are stored in `.env` and never committed to git. Every environment that needs them (including the Airflow container) gets them injected via `docker-compose.yaml`.
- Inside Docker, containers talk to each other using the service name (`db`) and internal port (`5432`), not the host machine port (`5000`).
