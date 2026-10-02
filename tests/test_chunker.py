from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.chunker import create_chunks


pdf_path = "data/research_paper.pdf"

# Step 1: Extract PDF text
pages = extract_text_from_pdf(pdf_path)

# Step 2: Create chunks
chunks = create_chunks(pages)

print("Pages extracted:", len(pages))
print("Chunks created:", len(chunks))


for i, chunk in enumerate(chunks[:5], start=1):

    print("\n================================")
    print("Chunk:", i)
    print("Page:", chunk["page"])
    print("Characters:", len(chunk["text"]))
    print("================================")

    print(chunk["text"][:300])