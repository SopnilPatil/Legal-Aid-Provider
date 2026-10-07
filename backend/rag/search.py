import json
import os
import faiss
import numpy as np

from rag.embedding_service import generate_embedding


# ==========================================
# PROJECT PATHS
# ==========================================

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

INDEX_PATH = os.path.join(
    BACKEND_DIR,
    "rag",
    "index",
    "legal_faiss.index"
)

METADATA_PATH = os.path.join(
    BACKEND_DIR,
    "rag",
    "index",
    "legal_metadata.json"
)

DATASET_PATH = os.path.join(
    PROJECT_ROOT,
    "Data",
    "unified_legal_dataset_cleaned.jsonl"
)


# ==========================================
# LOAD FAISS INDEX
# ==========================================

index = faiss.read_index(INDEX_PATH)


# ==========================================
# LOAD METADATA
# ==========================================

with open(
    METADATA_PATH,
    "r",
    encoding="utf-8"
) as file:

    metadata = json.load(file)


# ==========================================
# LOAD ORIGINAL LEGAL TEXT
# ==========================================

legal_records = {}

with open(
    DATASET_PATH,
    "r",
    encoding="utf-8"
) as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        record = json.loads(line)

        legal_records[record["id"]] = record


# ==========================================
# SEARCH FUNCTION
# ==========================================

def search_legal_provisions(
    query: str,
    top_k: int = 5
):

    # Generate query embedding
    query_embedding = generate_embedding(
        query
    )

    # FAISS expects 2D float32 array
    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    # Search
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx < 0:
            continue

        # Get metadata
        item = metadata[idx]

        record_id = item["id"]

        # Get original legal record
        record = legal_records.get(
            record_id
        )

        if not record:
            continue

        results.append({
            "score": float(score),
            "id": record_id,
            "text": record.get("text", ""),
            "metadata": record.get(
                "metadata",
                {}
            )
        })

    return results


# ==========================================
# TEST SEARCH
# ==========================================

if __name__ == "__main__":

    print("=" * 60)
    print("LEGAL AID PROVIDER - LEGAL SEARCH TEST")
    print("=" * 60)

    query = input(
        "\nEnter your legal question: "
    )

    results = search_legal_provisions(
        query,
        top_k=5
    )

    print(
        f"\nFound {len(results)} relevant provisions.\n"
    )

    for i, result in enumerate(
        results,
        start=1
    ):

        metadata_info = result["metadata"]

        print("-" * 60)

        print(
            f"RESULT {i}"
        )

        print(
            f"Similarity Score: {result['score']:.4f}"
        )

        print(
            f"ID: {result['id']}"
        )

        print(
            f"Law: {metadata_info.get('law_name')}"
        )

        print(
            f"Provision Type: "
            f"{metadata_info.get('provision_type')}"
        )

        print(
            f"Provision Number: "
            f"{metadata_info.get('provision_number')}"
        )

        print(
            f"Provision Title: "
            f"{metadata_info.get('provision_title')}"
        )

        print(
            f"\nLegal Text:\n"
            f"{result['text'][:1500]}"
        )

    print("\n" + "=" * 60)
    print("SEARCH COMPLETED")
    print("=" * 60)