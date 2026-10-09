# Build from the repo root: docker build -f apps/api/Dockerfile .
FROM python:3.13-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY packages/core /app/packages/core
COPY apps/api /app/apps/api
RUN pip install --no-cache-dir /app/packages/core /app/apps/api

RUN useradd --create-home sailprep
USER sailprep

EXPOSE 8000
CMD ["uvicorn", "sailprep_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
