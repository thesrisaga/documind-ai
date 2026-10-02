from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.chunker import create_chunks
from src.retrieval.retriever import Retriever
from src.generation.llm import LLM


pdf_path = "data/research_paper.pdf"


# 1. Extract PDF text
pages = extract_text_from_pdf(pdf_path)


# 2. Create text chunks
chunks = create_chunks(pages)


# 3. Create retriever
retriever = Retriever(chunks)


# 4. Initialize LLM
llm = LLM()


# 5. User question
question = "What factors influence successful stem cell differentiation?"


# 6. Retrieve relevant chunks
results = retriever.retrieve(
    question,
    top_k=5
)


# 7. Build context for the LLM
context_parts = []

for result in results:

    document = result["document"]

    context_parts.append(
        f"[Page {document['page']}]\n"
        f"{document['text']}"
    )


context = "\n\n".join(context_parts)


# 8. Generate answer
answer = llm.generate_answer(
    question,
    context
)


# 9. Display answer
print("\n================================")
print("DOCUMIND AI ANSWER")
print("================================")

print(answer)


# 10. Display sources
print("\n================================")
print("SOURCES")
print("================================")

pages_used = sorted(
    set(
        result["document"]["page"]
        for result in results
    )
)


for page in pages_used:

    print(
        f"research_paper.pdf — Page {page}"
    )