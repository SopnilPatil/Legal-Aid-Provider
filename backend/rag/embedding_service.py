from sentence_transformers import SentenceTransformer


# Embedding model
MODEL_NAME = "all-MiniLM-L6-v2"

# Load the model once when the service starts
model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str):
    """
    Convert text into a vector embedding.
    """

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding


def generate_embeddings(texts: list[str]):
    """
    Convert multiple texts into vector embeddings.
    """

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings