FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    numpy \
    faiss-cpu \
    sentence-transformers \
    rank-bm25 \
    langchain-text-splitters \
    qdrant-client
WORKDIR /app