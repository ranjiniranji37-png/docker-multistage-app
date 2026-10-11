# Student Notes App: Cloud Deployment and Monitoring Capstone



![CI-CD Pipeline](https://github.com/ranjiniranji37-png/docker-multistage-app/actions/workflows/ci-cd.yml/badge.svg)




![Docker Build and Test](https://github.com/ranjiniranji37-png/docker-multistage-app/actions/workflows/main.yml/badge.svg)



**Live cloud endpoint:** https://ranjinidevops.pythonanywhere.com
**Health check endpoint:** https://ranjinidevops.pythonanywhere.com/health

A Flask web app that is containerized with a multi-stage Docker build, tested and built by GitHub Actions, and deployed live on a cloud platform with uptime monitoring.

## Architecture

```
Developer -> GitHub (main branch)
                |
                v
        GitHub Actions CI/CD
        1. flake8 lint
        2. pytest unit tests
        3. Docker build and push to GitHub Container Registry (GHCR)
        4. docker compose test (web + PostgreSQL, health check, volume persistence)
                |
                v
   Live endpoint on PythonAnywhere  <---  UptimeRobot (checks /health every 5 minutes, email alerts)
```

## Repository contents

| File | Purpose |
|---|---|
| `app.py` | Flask app with `/`, `/health` and `/db` routes |
| `test_app.py` | Unit tests run by pytest |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Multi-stage build (134 MB final image), non-root user, HEALTHCHECK |
| `docker-compose.yml` | Web app and PostgreSQL with health checks and a named volume |
| `.github/workflows/main.yml` | Builds with Docker Compose and tests health, database and volume persistence |
| `.github/workflows/ci-cd.yml` | Lint, unit tests, image build and push to GHCR |
| `render.yaml` | Optional Render blueprint (not used for the final deployment) |

## Deployment

The live endpoint runs on PythonAnywhere as a Flask web app using the same `app.py` from this repository. Hugging Face Spaces and Render were tried first, but the free plans there were blocked by quota and card requirements.

The Docker image itself is built and published by the CI/CD pipeline to GitHub Container Registry, and it is tested end to end with Docker Compose in GitHub Actions.

## Environment variable configuration

The app reads `APP_ENV` and shows it in the home page response. It defaults to `production`.

- Docker Compose passes `DATABASE_URL` to the web service.
- GitHub Actions uses the built-in `GITHUB_TOKEN` to push images, so no passwords are stored in the code.

## Monitoring and health check alerts

- **Health endpoint:** `/health` returns `ok` with HTTP 200.
- **Docker HEALTHCHECK:** the container checks `/health` every 30 seconds.
- **UptimeRobot:** an HTTP(s) monitor checks the live `/health` URL every 5 minutes and sends an email alert when the app goes down.

## Run locally

```bash
docker compose up --build
curl http://localhost:5000/health
```

## Pipeline status

All GitHub Actions workflows pass with green checkmarks. See the **Actions** tab for build logs.
