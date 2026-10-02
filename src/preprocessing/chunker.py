def create_chunks(pages, chunk_size=800, overlap=150):
    """
    Split extracted PDF pages into smaller overlapping text chunks.

    Args:
        pages (list): Extracted PDF pages.
        chunk_size (int): Maximum number of characters in each chunk.
        overlap (int): Number of characters shared between consecutive chunks.

    Returns:
        list: Text chunks with page numbers.
    """

    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "page": page_number,
                    "text": chunk_text
                })

            start += chunk_size - overlap

    return chunks