import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

FILES = {
    "CONSTITUTION": (
        BASE_DIR
        / "Data"
        / "Indian Constitution"
        / "constitution_search_chunks.json"
    ),

    "BNS": (
        BASE_DIR
        / "Data"
        / "Bharatiya Nyay Sanhita"
        / "BNS_RAG_dataset"
        / "bns_rag.jsonl"
    ),

    "BNSS": (
        BASE_DIR
        / "Data"
        / "Bharatiya Nagarik Suraksha Sanhita"
        / "bnss_rag.jsonl"
    )
}


def inspect_json_array(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data[:3]


def inspect_jsonl(path):
    records = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

            if len(records) == 3:
                break

    return records


def show_record(record):

    print("\n" + "-" * 70)

    print("TOP-LEVEL KEYS:")
    print(list(record.keys()))

    print("\nFULL RECORD:")

    print(
        json.dumps(
            record,
            indent=2,
            ensure_ascii=False
        )
    )


def main():

    print("=" * 70)
    print("LEGAL DATASET STRUCTURE INSPECTOR")
    print("=" * 70)

    for name, path in FILES.items():

        print("\n\n" + "=" * 70)
        print(name)
        print("=" * 70)

        print("\nFILE:")
        print(path)

        if not path.exists():

            print("\n❌ FILE NOT FOUND")
            continue

        print("\n✅ FILE FOUND")

        if path.suffix.lower() == ".json":

            records = inspect_json_array(path)

        else:

            records = inspect_jsonl(path)

        print(
            f"\nShowing first {len(records)} records:"
        )

        for record in records:
            show_record(record)


if __name__ == "__main__":
    main()