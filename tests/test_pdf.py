from src.ingestion.pdf_loader import extract_text_from_pdf


pdf_path = "data/research_paper.pdf"

pages = extract_text_from_pdf(pdf_path)

print("Number of pages extracted:", len(pages))

for page in pages[:2]:

    print("\n==============================")
    print("Page:", page["page"])
    print("==============================")

    print(page["text"][:500])