# Python stable version (권장: 3.10)
FROM python:3.10-slim

# Prevent Python from writing .pyc and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# OS dependencies (pyhwp + XML/XSLT + zlib 계열 안정화)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 \
    libxslt1.1 \
    zlib1g \
    && rm -rf /var/lib/apt/lists/*

# 1) Install Python deps first (Docker layer cache 활용)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# 2) Copy application source code from local drive -> container
COPY src/ /app/src/

# 기본 실행 (원하면 CMD를 바꿔도 됨)
ENTRYPOINT ["python", "-m", "src.main"]
