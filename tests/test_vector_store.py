from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.chunker import create_chunks
from src.embeddings.embedding_model import EmbeddingModel
from src.retrieval.vector_store import VectorStore


# --------------------------------
# 1. Load PDF
# --------------------------------

pdf_path = "data/research_paper.pdf"

pages = extract_text_from_pdf(pdf_path)


# --------------------------------
# 2. Create chunks
# --------------------------------

chunks = create_chunks(pages)


# --------------------------------
# 3. Extract chunk text
# --------------------------------

texts = [
    chunk["text"]
    for chunk in chunks
]


# --------------------------------
# 4. Generate embeddings
# --------------------------------

embedding_model = EmbeddingModel()

embeddings = embedding_model.generate_embeddings(
    texts
)


# --------------------------------
# 5. Create vector store
# --------------------------------

dimension = embeddings.shape[1]

vector_store = VectorStore(
    dimension
)


# --------------------------------
# 6. Add documents
# --------------------------------

vector_store.add_documents(
    embeddings,
    chunks
)


# --------------------------------
# 7. Create query
# --------------------------------

question = "What factors affect stem cell differentiation?"


# --------------------------------
# 8. Convert query into embedding
# --------------------------------

query_embedding = embedding_model.generate_embeddings(
    [question]
)[0]


# --------------------------------
# 9. Search
# --------------------------------

results = vector_store.search(
    query_embedding,
    top_k=5
)


# --------------------------------
# 10. Display results
# --------------------------------

print("\n================================")
print("SEMANTIC SEARCH RESULTS")
print("================================")

print("Question:", question)


for i, result in enumerate(results, start=1):

    document = result["document"]

    print("\n--------------------------------")
    print("Result:", i)
    print("Page:", document["page"])
    print("Distance:", result["distance"])
    print("--------------------------------")

    print(
        document["text"][:500]
    )