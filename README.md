# Python FastAPI — Docker & Kubernetes Deployment

A minimal FastAPI application demonstrating a complete production-grade workflow: local development → Docker container → Kubernetes cluster, with automated CI/CD via GitHub Actions.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker](#docker)
- [Kubernetes](#kubernetes)
- [CI/CD Pipeline](#cicd-pipeline)
- [Configuration & Secrets](#configuration--secrets)

---

## Overview

| Layer | Technology |
|---|---|
| Application | Python 3.11 + FastAPI + Uvicorn |
| Container | Docker (image: `debasishdocker2025/my-python-api`) |
| Orchestration | Kubernetes (Deployment + NodePort Service) |
| CI/CD | GitHub Actions → Docker Hub |

Every push to `main` automatically builds a new Docker image, tags it with both `latest` and the commit SHA, and pushes it to Docker Hub.

---

## Project Structure

```
python-app/
├── main.py                      # FastAPI application
├── requirements.txt             # Python dependencies
├── dockerfile                   # Container build instructions
├── k8s-deployment.yaml          # Kubernetes Deployment + Service manifest
└── .github/
    └── workflows/
        └── ci-cd.yml            # GitHub Actions CI/CD pipeline
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Returns a hello-world JSON response |
| `GET` | `/health` | Health check — returns `{"status": "healthy"}` |

**Root response:**
```json
{"message": "Hello World! Our API is up and running."}
```

**Health check response:**
```json
{"status": "healthy"}
```

FastAPI also auto-generates interactive docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Local development |
| Docker | Latest | Build & run containers |
| kubectl | Latest | Interact with Kubernetes |
| minikube / kind | Latest | Local Kubernetes cluster (dev) |

---

## Local Development

```bash
# 1. Clone the repository
git clone https://github.com/DebasishBiswas1/python-app.git
cd python-app

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

---

## Docker

### Build the image locally

```bash
docker build -t my-python-api:latest .
```

### Run the container

```bash
docker run -d -p 8000:8000 --name python-api my-python-api:latest
```

The API will be available at `http://localhost:8000`.

### Stop and remove the container

```bash
docker stop python-api && docker rm python-api
```

### Pull the published image from Docker Hub

```bash
docker pull debasishdocker2025/my-python-api:latest
```

---

## Kubernetes

The `k8s-deployment.yaml` file defines two Kubernetes resources:

| Resource | Name | Details |
|---|---|---|
| `Deployment` | `python-api-deployment` | 2 replicas of the container |
| `Service` | `python-api-service` | `NodePort` exposing port `30080` |

### Deploy to the cluster

```bash
kubectl apply -f k8s-deployment.yaml
```

### Verify the deployment

```bash
# Check pods are running
kubectl get pods

# Check the service
kubectl get services

# View deployment details
kubectl describe deployment python-api-deployment
```

### Access the application

| Environment | URL |
|---|---|
| minikube | `http://$(minikube ip):30080` |
| Docker Desktop | `http://localhost:30080` |
| Cloud cluster | `http://<node-external-ip>:30080` |

### Scale the deployment

```bash
# Scale up to 4 replicas
kubectl scale deployment python-api-deployment --replicas=4

# Scale back down
kubectl scale deployment python-api-deployment --replicas=2
```

### Update to a new image

```bash
kubectl set image deployment/python-api-deployment \
  python-api-container=debasishdocker2025/my-python-api:<new-tag>
```

### Tear down

```bash
kubectl delete -f k8s-deployment.yaml
```

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) runs on every push to `main`.

```
Push to main
    │
    ▼
Checkout code
    │
    ▼
Log in to Docker Hub (using repository secrets)
    │
    ▼
Build Docker image
    │
    ▼
Push two tags to Docker Hub:
  • debasishdocker2025/my-python-api:latest
  • debasishdocker2025/my-python-api:<commit-sha>
```

The commit-SHA tag ensures every build is uniquely identifiable and traceable back to a specific commit.

---

## Configuration & Secrets

The pipeline requires two GitHub repository secrets:

| Secret | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | A Docker Hub access token (not your password) |

### Setting up secrets

1. Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`

To generate a Docker Hub access token: Docker Hub → **Account Settings** → **Personal access tokens** → **Generate new token** (set scope to **Read & Write**).
