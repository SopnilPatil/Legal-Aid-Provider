import json
import os

from backend.rag.embedding_service import generate_embeddings


# ==========================================
# PATHS
# ==========================================

DATASET_PATH = os.path.join(
    "Data",
    "unified_legal_dataset_Cleaned.jsonl"
)

OUTPUT_DIR = os.path.join(
    "rag",
    "index"
)

EMBEDDINGS_PATH = os.path.join(
    OUTPUT_DIR,
    "legal_embeddings.npy"
)

METADATA_PATH = os.path.join(
    OUTPUT_DIR,
    "legal_metadata.json"
)


# ==========================================
# LOAD DATASET
# ==========================================

def load_dataset():

    records = []

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

            records.append(record)

    return records


# ==========================================
# MAIN
# ==========================================

def main():

    print("=" * 60)
    print("LEGAL AID PROVIDER - EMBEDDING GENERATION")
    print("=" * 60)

    # Load records
    records = load_dataset()

    print(f"\nLoaded records: {len(records)}")

    if not records:
        raise ValueError("No records found in dataset.")

    # Extract legal text
    texts = [
        record["search_text"]
        for record in records
    ]

    print("\nGenerating embeddings...")
    print("This may take some time on the first run.\n")

    # Generate embeddings
    embeddings = generate_embeddings(texts)

    print("\nEmbedding generation completed.")

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    # Create output directory
    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    # Save embeddings
    import numpy as np

    np.save(
        EMBEDDINGS_PATH,
        embeddings
    )

    # Save metadata
    metadata = []

    for record in records:

        metadata.append({
            "id": record.get("id"),
            "metadata": record.get("metadata", {})
        })

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\nFiles saved:")
    print(f"Embeddings : {EMBEDDINGS_PATH}")
    print(f"Metadata   : {METADATA_PATH}")

    print("\n" + "=" * 60)
    print("EMBEDDING GENERATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()