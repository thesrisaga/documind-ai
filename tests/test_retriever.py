from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.chunker import create_chunks
from src.retrieval.retriever import Retriever


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
# 3. Create retriever
# --------------------------------

retriever = Retriever(chunks)


# --------------------------------
# 4. Ask a question
# --------------------------------

question = "What factors influence successful stem cell differentiation?"


# --------------------------------
# 5. Retrieve relevant chunks
# --------------------------------

results = retriever.retrieve(
    question,
    top_k=5
)


# --------------------------------
# 6. Display results
# --------------------------------

print("\n================================")
print("DOCUMIND RETRIEVER")
print("================================")

print("\nQuestion:")
print(question)


for i, result in enumerate(results, start=1):

    document = result["document"]

    print("\n--------------------------------")
    print("Result:", i)
    print("Page:", document["page"])
    print("Distance:", result["distance"])
    print("--------------------------------")

    print(document["text"][:500])