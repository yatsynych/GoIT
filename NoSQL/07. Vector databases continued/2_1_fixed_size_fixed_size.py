from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

text = """
Large language models have transformed natural language processing. They are trained
on vast corpora of text and can perform tasks ranging from translation to code generation.
BERT introduced bidirectional context modelling, while GPT-style models use causal
(left-to-right) attention. The scaling laws suggest that larger models trained on more data
tend to perform better across benchmarks. However, inference costs scale accordingly,
making efficient deployment a critical engineering challenge.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""],
)

chunks = splitter.split_text(text.strip())
for i, chunk in enumerate(chunks):
    print(f"--- Chunk{i+1} ({len(chunk)} chars) ---")
    print(chunk[:120])
    print()