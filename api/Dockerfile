FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .

# The key fix is the --prefix=/install flag below
RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Security updates
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Copy from the builder stage
COPY --from=builder /install /usr/local
COPY . .

RUN useradd -m -u 1001 appuser
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]