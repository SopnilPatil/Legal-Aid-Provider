import json
import re
import os

DATASET_PATH = os.path.join(
    "Data",
    "unified_legal_dataset_cleaned.jsonl"
)

pattern = re.compile(
    r"\.{2,}|(?:\.\s*){3,}"
)

count = 0

with open(DATASET_PATH, "r", encoding="utf-8") as file:

    for line in file:

        record = json.loads(line)

        search_text = record.get("search_text", "")

        matches = pattern.findall(search_text)

        if matches:

            count += 1

            print("=" * 60)
            print("ID:", record.get("id"))
            print("Law:", record.get("metadata", {}).get("law_name"))
            print(
                "Provision:",
                record.get("metadata", {}).get("provision_number")
            )

            print("\nDot patterns found:")

            for match in matches[:10]:
                print(repr(match))

            print("\nText sample:")
            print(search_text[:1000])

            if count >= 20:
                break

print("\n" + "=" * 60)
print("Records inspected:", count)
print("=" * 60)