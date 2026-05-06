# Phase 5: Plus (Docker, K8s, CI/CD, Terraform)

**Prerequisite:** Phase 4 complete. FastAPI and WebSockets already known (PerfumeShop + Loopgate).
**Goal:** Containerization, orchestration, automation, infra-as-code.

---

## Part A: Docker

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Dockerfile | "What is a Dockerfile? What are the key instructions?" | [ ] |
| multi-stage builds | "What is a multi-stage Docker build? Why use it?" | [ ] |
| image layers | "How do Docker image layers work? Why does layer order matter?" | [ ] |
| docker-compose | "What is docker-compose? When do you use it?" | [ ] |
| .dockerignore | "What goes in .dockerignore?" | [ ] |

**Exercise:** Dockerize PerfumeShop AI:
```dockerfile
# Dockerfile
FROM python:3.11-slim AS base
WORKDIR /app

FROM base AS deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM deps AS final
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Add `docker-compose.yml` that mounts `.env` and `data/` as volumes.

**Tricky question Claude will ask:** "Why is `COPY requirements.txt .` before `COPY . .`? What breaks if you swap them?"

**Resources:** [Docker Python best practices](https://docs.docker.com/guides/python/)

---

## Part B: Kubernetes (Conceptual + Basic)

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Pod | "What is a Kubernetes Pod?" | [ ] |
| Deployment | "What is a Deployment? How does it differ from a Pod?" | [ ] |
| Service | "What is a Kubernetes Service? Types?" | [ ] |
| Ingress | "What is an Ingress? How does it route traffic?" | [ ] |
| ConfigMap / Secret | "How do you pass config/secrets to a Pod?" | [ ] |
| HPA | "What is Horizontal Pod Autoscaling?" | [ ] |
| EKS | "What is EKS? How does it relate to K8s?" | [ ] |

**Exercise:** Write Kubernetes manifests for PerfumeShop:
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: perfumeshop-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: perfumeshop
  template:
    metadata:
      labels:
        app: perfumeshop
    spec:
      containers:
      - name: api
        image: perfumeshop:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: perfumeshop-secrets
```

Add a Service + Ingress. Don't deploy — just write and review with Claude.

**Resources:** [Kubernetes docs – Concepts](https://kubernetes.io/docs/concepts/)

---

## Part C: GitHub Actions CI/CD

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| workflow syntax | "What is a GitHub Actions workflow?" | [ ] |
| jobs and steps | "What is the difference between a job and a step?" | [ ] |
| triggers | "What triggers can start a GitHub Actions workflow?" | [ ] |
| secrets | "How do you use secrets in GitHub Actions?" | [ ] |
| artifact caching | "How do you cache dependencies in GitHub Actions?" | [ ] |
| matrix builds | "What is a matrix strategy in GitHub Actions?" | [ ] |

**Exercise:** Create `.github/workflows/ci.yml` for PerfumeShop:
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=src --cov-fail-under=70
      - run: ruff check .
```

**Resources:** [GitHub Actions docs](https://docs.github.com/en/actions)

---

## Part D: Terraform

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| HCL syntax | "What is Terraform HCL? What are resources and data sources?" | [ ] |
| state file | "What is Terraform state? Why store it remotely?" | [ ] |
| plan / apply | "What is terraform plan? Why run it before apply?" | [ ] |
| modules | "What is a Terraform module?" | [ ] |
| AWS provider | "How do you configure the AWS provider in Terraform?" | [ ] |

**Exercise:** Create `infra/main.tf` for PerfumeShop S3 bucket:
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "perfumeshop/terraform.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "embeddings" {
  bucket = "perfumeshop-embeddings-${var.environment}"
}

variable "environment" {
  type    = string
  default = "dev"
}
```

Do NOT run `terraform apply` without reviewing costs. Review the plan with Claude first.

**Resources:** [Terraform AWS Provider docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

## Part E: FastAPI Advanced + WebSockets (Loopgate)

> FastAPI basics already known. Focus on what Loopgate adds.

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| WebSockets in FastAPI | "How do you implement WebSockets in FastAPI?" | [ ] |
| connection manager | "How do you manage multiple WebSocket connections?" | [ ] |
| Background tasks | "What is FastAPI BackgroundTasks?" | [ ] |
| Middleware | "How do you add middleware in FastAPI?" | [ ] |

**Exercise:** Explain Loopgate's WebSocket architecture to Claude:
- Where is the human approval gate?
- How does the agent pause while waiting for human input?
- What happens if the human never approves? (timeout)

This prepares you to explain human-in-the-loop in an interview using your own project.

---

## Completion Criteria

- [ ] PerfumeShop Docker image builds and runs locally
- [ ] `docker-compose.yml` starts the full stack
- [ ] K8s manifests (Deployment + Service + Ingress) written and reviewed
- [ ] `.github/workflows/ci.yml` passing on push to main
- [ ] `infra/main.tf` for S3 bucket written (not applied)
- [ ] Can explain K8s pod/deployment/service in 2 sentences each
- [ ] Can explain WebSocket flow in Loopgate clearly in interview
