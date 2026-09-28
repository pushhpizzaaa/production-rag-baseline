# Production Docker Containerization Best Practices

**Doc ID:** `fastapi_docker_containerization_best_practices`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Build lightweight, secure multi-stage Docker images for FastAPI deployments.

---

## Multi-Stage Dockerfile
```dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./src ./src
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
USER 1000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
Runs as non-root user for security compliance.

