import json
import os
import re


INPUT_PATH = os.path.join(
    "Data",
    "unified_legal_dataset.jsonl"
)

OUTPUT_PATH = os.path.join(
    "Data",
    "unified_legal_dataset_cleaned.jsonl"
)

def clean_for_search(text: str) -> str:
    """
    Create a search-friendly version of legal text.

    The original legal text is never modified.
    """

    if not text:
        return ""

    cleaned = text

    # --------------------------------------------------
    # 1. Remove long dot placeholders
    # Example:
    # Name......................
    # --------------------------------------------------
    cleaned = re.sub(r"\.{5,}", " ", cleaned)

    # --------------------------------------------------
    # 2. Remove 2-4 consecutive dots when they are being
    # used as layout/form placeholders.
    #
    # We deliberately avoid touching normal single periods.
    # --------------------------------------------------
    cleaned = re.sub(r"(?<!\.)\.{2,}(?!\.)", " ", cleaned)

    # --------------------------------------------------
    # 3. Remove spaced dot placeholders
    #
    # Examples:
    # . . . . .
    # . . . . . . .
    # --------------------------------------------------
    cleaned = re.sub(
        r"(?:\.\s*){3,}",
        " ",
        cleaned
    )

    # --------------------------------------------------
    # 4. Remove excessive underscores used as blank fields
    # --------------------------------------------------
    cleaned = re.sub(r"_{5,}", " ", cleaned)

    # --------------------------------------------------
    # 5. Remove very long hyphen placeholders
    # --------------------------------------------------
    cleaned = re.sub(r"-{8,}", " ", cleaned)

    # --------------------------------------------------
    # 6. Normalize tabs
    # --------------------------------------------------
    cleaned = cleaned.replace("\t", " ")

    # --------------------------------------------------
    # 7. Normalize repeated spaces
    # --------------------------------------------------
    cleaned = re.sub(r"[ ]{2,}", " ", cleaned)

    # --------------------------------------------------
    # 8. Normalize excessive blank lines
    # --------------------------------------------------
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()


def main():

    print("=" * 60)
    print("LEGAL AID PROVIDER - SEARCH TEXT CLEANING")
    print("=" * 60)

    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_PATH}"
        )

    records = []

    print("\nLoading original dataset...")

    with open(INPUT_PATH, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            record = json.loads(line)

            # Keep original text exactly as it is.
            original_text = record.get("text", "")

            # Create separate search version.
            search_text = clean_for_search(original_text)

            record["search_text"] = search_text

            records.append(record)

    print(f"Records loaded: {len(records)}")

    # Create output directory if required.
    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True
    )

    print("\nSaving cleaned dataset...")

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        for record in records:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    print("\nCleaning completed.")

    print(f"Original dataset:")
    print(f"  {INPUT_PATH}")

    print(f"\nCleaned dataset:")
    print(f"  {OUTPUT_PATH}")

    print("\nOriginal legal text has NOT been changed.")

    print("\n" + "=" * 60)
    print("SEARCH TEXT CLEANING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()