import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    BASE_DIR
    / "Data"
    / "unified_legal_dataset.jsonl"
)


def main():

    missing = []

    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            if not line.strip():
                continue

            record = json.loads(line)

            metadata = record.get(
                "metadata",
                {}
            )

            if (
                metadata.get("law_code") == "BNSS"
                and metadata.get("provision_type") == "section"
                and not metadata.get("provision_title")
            ):

                missing.append(record)


    print("=" * 70)
    print("BNSS RECORDS WITH MISSING SECTION TITLES")
    print("=" * 70)

    print(
        f"\nTotal missing titles: {len(missing)}"
    )


    for record in missing:

        metadata = record[
            "metadata"
        ]

        print("\n" + "-" * 70)

        print(
            "ID:",
            record.get("id")
        )

        print(
            "Section:",
            metadata.get(
                "provision_number"
            )
        )

        print(
            "Chapter:",
            metadata.get(
                "chapter_number"
            )
        )

        print(
            "Chapter title:",
            metadata.get(
                "chapter_title"
            )
        )

        print("\nText preview:")

        print(
            record.get(
                "text",
                ""
            )[:500]
            .replace("\n", " ")
        )


if __name__ == "__main__":
    main()