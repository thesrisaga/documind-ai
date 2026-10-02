import pymupdf


def extract_text_from_pdf(pdf_path):
    """
    Extract text from every page of a PDF.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list: A list containing page numbers and extracted text.
    """

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number in range(document.page_count):

        page = document.load_page(page_number)

        text = str(page.get_text("text"))

        if text.strip():

            pages.append({
                "page": page_number + 1,
                "text": text.strip()
            })

    document.close()

    return pages