from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import os



def semantic_chunking(
    text: str,
    model: SentenceTransformer,
    threshold: float = 0.7,
    min_chunk_size: int = 50,
) -> List[str]:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    if len(sentences) < 2:
        return sentences

    embeddings = model.encode(sentences, normalize_embeddings=True)
    similarities = [
        float(np.dot(embeddings[i], embeddings[i + 1]))
        for i in range(len(embeddings) - 1)
    ]

    chunks = []
    current_chunk = [sentences[0]]
    for i, sim in enumerate(similarities):
        if sim < threshold and len(" ".join(current_chunk)) >= min_chunk_size:
            chunks.append(". ".join(current_chunk) + ".")
            current_chunk = [sentences[i + 1]]
        else:
            current_chunk.append(sentences[i + 1])

    if current_chunk:
        chunks.append(". ".join(current_chunk) + ".")
    return chunks


text = """
This is an example text to test semantic chunking.
Each sentence will be evaluated for similarity with its neighbors.
If the similarity is low, a new chunk begins.
This way, long texts can be divided into meaningful segments.
Semantic chunking is useful for summarization and topic analysis.
"""

model = SentenceTransformer("all-MiniLM-L6-v2")
chunks = semantic_chunking(text.strip(), model, threshold=0.6)

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

for i, chunk in enumerate(chunks):
    print(f"\n[Chunk{i+1}]\n{chunk}")