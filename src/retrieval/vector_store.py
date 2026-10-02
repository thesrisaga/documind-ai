import faiss
import numpy as np


class VectorStore:
    """
    Store and search document embeddings using FAISS.
    """

    def __init__(self, dimension):
        """
        Initialize the FAISS vector index.

        Args:
            dimension (int): Number of dimensions in each embedding.
        """

        self.index = faiss.IndexFlatL2(dimension)

        self.documents = []


    def add_documents(self, embeddings, documents):
        """
        Add embeddings and their corresponding documents.

        Args:
            embeddings: Numpy array containing document embeddings.
            documents: List of document chunks.
        """

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)

        self.documents.extend(documents)


    def search(self, query_embedding, top_k=5):
        """
        Search for the most similar document chunks.

        Args:
            query_embedding: Embedding of the user's question.
            top_k (int): Number of results to return.

        Returns:
            list: Most relevant document chunks.
        """

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index != -1:

                results.append({
                    "document": self.documents[index],
                    "distance": float(distance)
                })

        return results