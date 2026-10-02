from src.embeddings.embedding_model import EmbeddingModel
from src.retrieval.vector_store import VectorStore


class Retriever:
    """
    Retrieve the most relevant document chunks
    for a user's question.
    """

    def __init__(self, chunks):
        """
        Initialize the retriever.

        Args:
            chunks (list): Document chunks containing
                           page number and text.
        """

        self.chunks = chunks

        self.embedding_model = EmbeddingModel()

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.embedding_model.generate_embeddings(
            texts
        )

        dimension = embeddings.shape[1]

        self.vector_store = VectorStore(
            dimension
        )

        self.vector_store.add_documents(
            embeddings,
            chunks
        )

    def retrieve(self, question, top_k=5):
        """
        Retrieve the most relevant chunks for a question.

        Args:
            question (str): User's question.
            top_k (int): Number of chunks to retrieve.

        Returns:
            list: Relevant document chunks.
        """

        query_embedding = (
            self.embedding_model
            .generate_embeddings([question])[0]
        )

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        return results