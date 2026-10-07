import os
import numpy as np
import faiss


# ==========================================
# PATHS
# ==========================================

EMBEDDINGS_PATH = os.path.join(
    "rag",
    "index",
    "legal_embeddings.npy"
)

INDEX_PATH = os.path.join(
    "rag",
    "index",
    "legal_faiss.index"
)


# ==========================================
# BUILD FAISS INDEX
# ==========================================

def main():

    print("=" * 60)
    print("LEGAL AID PROVIDER - FAISS INDEX CREATION")
    print("=" * 60)

    # Load embeddings
    print("\nLoading embeddings...")

    embeddings = np.load(
        EMBEDDINGS_PATH
    )

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    # Make sure FAISS receives float32
    embeddings = embeddings.astype(
        "float32"
    )

    # Number of dimensions
    dimension = embeddings.shape[1]

    print(
        f"Vector dimension: {dimension}"
    )

    # Create FAISS index
    #
    # Because our embeddings are normalized,
    # Inner Product works as cosine similarity.
    index = faiss.IndexFlatIP(
        dimension
    )

    print("\nAdding embeddings to FAISS...")

    index.add(
        embeddings
    )

    print(
        f"Vectors stored in index: {index.ntotal}"
    )

    # Save index
    faiss.write_index(
        index,
        INDEX_PATH
    )

    print(
        f"\nFAISS index saved to: {INDEX_PATH}"
    )

    print("\n" + "=" * 60)
    print("FAISS INDEX CREATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()