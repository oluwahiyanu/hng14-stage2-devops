# HNG Stage 2 — Containerized Job Processing System

A production-ready microservices application containerized with Docker, orchestrated with Docker Compose, and deployed via a full CI/CD pipeline on GitHub Actions.

---

## Architecture

```
                    ┌─────────────────────────────────────────┐
                    │           Internal Docker Network        │
                    │                                         │
  Browser ──► :3000 │  Frontend (Node.js)                     │
                    │       │                                  │
                    │       ▼                                  │
                    │  API (FastAPI) ──► Redis ◄── Worker      │
                    │                                         │
                    └─────────────────────────────────────────┘
```

| Service  | Language       | Internal Port | Description                        |
|----------|----------------|---------------|------------------------------------|
| frontend | Node.js/Express| 3000          | Web UI — submits and tracks jobs   |
| api      | Python/FastAPI | 8000          | REST API — creates and reads jobs  |
| worker   | Python         | —             | Background processor — runs jobs   |
| redis    | Redis 7        | 6379          | Message queue and state store      |

Redis is **not exposed** on the host. Only the frontend is accessible publicly on port 3000.

---

## Prerequisites

Make sure the following are installed on your machine before starting:

- [Docker](https://docs.docker.com/get-docker/) v24+
- [Docker Compose](https://docs.docker.com/compose/install/) v2.20+
- [Git](https://git-scm.com/)

Verify installations:
```bash
docker --version
docker compose version
git --version
```

---

## Quick Start (Clean Machine)

### 1. Clone the repository

```bash
git clone https://github.com/oluwahiyanu/hng14-stage2-devops.git
cd hng14-stage2-devops
```

### 2. Create your environment file

```bash
cp .env.example .env
```

Open `.env` and fill in your values — see [Environment Variables](#environment-variables) below.

### 3. Build and start the stack

```bash
docker compose up -d --build
```

This will:
- Build all three service images from their Dockerfiles
- Pull the Redis 7 Alpine image
- Start all services in dependency order (Redis → API + Worker → Frontend)
- Run health checks before marking each service ready

### 4. Verify everything is running

```bash
docker compose ps
```

A successful startup looks like this:

```
NAME                    STATUS                   PORTS
stage2-redis-1          Up (healthy)
stage2-api-1            Up (healthy)
stage2-worker-1         Up
stage2-frontend-1       Up (healthy)             0.0.0.0:3000->3000/tcp
```

All services should show `Up` and the three with health checks should show `healthy`. If any show `starting`, wait 30 seconds and run `docker compose ps` again.

### 5. Open the application

Visit **http://localhost:3000** in your browser.

Click **Submit New Job** — a job ID will appear and the status will update from `queued` to `completed` within a few seconds.

---

## API Endpoints

The API runs internally on port 8000. It is proxied through the frontend and not directly exposed.

### `GET /health`
Returns service health status.
```json
{"status": "healthy"}
```

### `POST /jobs`
Creates a new job and queues it for processing.
```json
{"job_id": "550e8400-e29b-41d4-a716-446655440000"}
```

### `GET /jobs/{job_id}`
Returns the current status of a job.
```json
{"job_id": "550e8400-e29b-41d4-a716-446655440000", "status": "queued"}
```
Possible status values: `queued` → `completed`

---

## Environment Variables

All configuration is driven by environment variables. Never hardcode values in source files.

| Variable     | Description                          | Example                  |
|--------------|--------------------------------------|--------------------------|
| `REDIS_HOST` | Hostname of the Redis service        | `redis`                  |
| `REDIS_PORT` | Port Redis listens on                | `6379`                   |
| `API_URL`    | Internal URL the frontend uses to reach the API | `http://api:8000` |

See `.env.example` for a ready-to-copy template.

---

## Running Tests Locally

```bash
cd api
pip install -r requirements.txt
pip install pytest pytest-cov
pytest tests/ -v --cov=. --cov-report=term
```

The test suite has 4 tests covering:
- Health endpoint returns 200 and correct JSON
- Job creation returns a job ID
- Job status retrieval returns correct status
- Missing job returns error response

All tests mock Redis — no running Redis instance is needed.

---

## CI/CD Pipeline

The pipeline runs automatically on every push and pull request via GitHub Actions.

### Stages (run in strict order)

```
lint → test → build → security scan → integration test → deploy
```

| Stage            | What it does                                                                 |
|------------------|------------------------------------------------------------------------------|
| **lint**         | Runs flake8 (Python), eslint (JavaScript), hadolint (Dockerfiles)           |
| **test**         | Runs pytest with Redis mocked, uploads coverage report as artifact           |
| **build**        | Builds all 3 images, tags with git SHA + latest, pushes to local registry   |
| **security**     | Scans all images with Trivy, fails on any CRITICAL finding, uploads SARIF   |
| **integration**  | Brings full stack up, submits a job, polls until completed, tears down      |
| **deploy**       | Rolling update on push to `main` only — new container must pass healthcheck before old one stops |

A failure at any stage stops all subsequent stages from running.

### Required GitHub Secrets

Set these in your repo under **Settings → Secrets and variables → Actions**:

| Secret            | Value                                      |
|-------------------|--------------------------------------------|
| `SERVER_HOST`     | Your server's public IP or domain          |
| `SERVER_USER`     | `hngdevops`                                |
| `SSH_PRIVATE_KEY` | Contents of your `~/.ssh/id_rsa` private key |

---

## Stopping the Stack

```bash
# Stop all containers
docker compose down

# Stop and remove all volumes (clears Redis data)
docker compose down -v

# Remove built images as well
docker compose down -v --rmi all
```

---

## Viewing Logs

```bash
# All services
docker compose logs -f

# Single service
docker compose logs -f api
docker compose logs -f worker
docker compose logs -f frontend
```

---

## Project Structure

```
.
├── api/
│   ├── Dockerfile          # Multi-stage Python image, non-root user
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── tests/
│       └── test_api.py     # pytest unit tests (Redis mocked)
├── worker/
│   ├── Dockerfile          # Multi-stage Python image, non-root user
│   ├── worker.py           # Job processor
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile          # Multi-stage Node.js image, non-root user
│   ├── app.js              # Express application
│   ├── package.json
│   └── views/
│       └── index.html      # Job dashboard UI
├── .github/
│   └── workflows/
│       └── pipeline.yml    # Full CI/CD pipeline
├── docker-compose.yml      # Full stack orchestration
├── .env.example            # Template for environment variables
├── FIXES.md                # All bugs found and fixed
└── README.md               # This file
```

---

## Live Deployment

**URL:** https://oluwahiyanu.mooo.com

**GitHub Repository:** https://github.com/oluwahiyanu/hng14-stage2-devops
