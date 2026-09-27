FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create the non-root user first
RUN useradd --create-home --shell /bin/bash appuser

COPY requirements.txt /app/
COPY aip-sdk/ /app/aip-sdk/

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install -r /app/requirements.txt && \
    pip install --no-cache-dir /app/aip-sdk/*.whl

COPY --chown=appuser:appuser . /app


USER appuser

CMD ["bash"]