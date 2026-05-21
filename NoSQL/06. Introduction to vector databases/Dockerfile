FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    sentence-transformers \
    numpy \
    scikit-learn \
    chromadb \
    qdrant-client \
    pinecone

WORKDIR /app