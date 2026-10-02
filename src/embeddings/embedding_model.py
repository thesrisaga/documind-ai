from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Generate numerical vector representations
    for text using a Sentence Transformer model.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def generate_embeddings(self, texts):
        """
        Convert a list of text chunks into embeddings.

        Args:
            texts (list): List of text strings.

        Returns:
            numpy.ndarray: Embedding vectors.
        """

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings