from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.chunker import create_chunks
from src.embeddings.embedding_model import EmbeddingModel


# PDF path
pdf_path = "data/research_paper.pdf"


# Step 1: Extract text
pages = extract_text_from_pdf(pdf_path)


# Step 2: Create chunks
chunks = create_chunks(pages)


# Step 3: Get the text from each chunk
texts = [
    chunk["text"]
    for chunk in chunks
]


# Step 4: Create embedding model
embedding_model = EmbeddingModel()


# Step 5: Generate embeddings
embeddings = embedding_model.generate_embeddings(
    texts
)


# Display results
print("\n==============================")
print("EMBEDDING TEST")
print("==============================")

print("Number of chunks:", len(chunks))

print(
    "Embedding shape:",
    embeddings.shape
)

print(
    "First embedding dimension:",
    len(embeddings[0])
)

print(
    "First 10 values:",
    embeddings[0][:10]
)