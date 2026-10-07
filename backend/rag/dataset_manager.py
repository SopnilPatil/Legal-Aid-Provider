import json
import os


# ============================================================
# DATASET PATHS
# ============================================================

CORE_DATASET = os.path.join(
    "Data",
    "unified_legal_dataset_cleaned.jsonl"
)

ACTS_DIRECTORY = os.path.join(
    "Data",
    "Acts"
)


# ============================================================
# LOAD JSONL DATASET
# ============================================================

def load_jsonl(file_path: str):
    records = []

    if not os.path.exists(file_path):
        print(f"WARNING: Dataset not found: {file_path}")
        return records

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
                records.append(record)

            except json.JSONDecodeError as e:

                print(
                    f"WARNING: Invalid JSON in {file_path}: {e}"
                )

    return records


# ============================================================
# LOAD CORE LEGAL DATASETS
# ============================================================

def load_core_dataset():

    print("\nLoading core legal dataset...")

    records = load_jsonl(CORE_DATASET)

    print(
        f"Core legal records loaded: {len(records)}"
    )

    return records


# ============================================================
# DISCOVER ACT DATASETS
# ============================================================

def discover_act_datasets():

    datasets = []

    if not os.path.exists(ACTS_DIRECTORY):

        print(
            f"WARNING: Acts directory not found: "
            f"{ACTS_DIRECTORY}"
        )

        return datasets

    for act_name in sorted(
        os.listdir(ACTS_DIRECTORY)
    ):

        act_directory = os.path.join(
            ACTS_DIRECTORY,
            act_name
        )

        if not os.path.isdir(act_directory):
            continue

        # Find JSONL files inside the Act folder.
        for filename in sorted(
            os.listdir(act_directory)
        ):

            if not filename.lower().endswith(".jsonl"):
                continue

            file_path = os.path.join(
                act_directory,
                filename
            )

            datasets.append({
                "act_name": act_name,
                "file_path": file_path
            })

    return datasets


# ============================================================
# LOAD ALL ACT DATASETS
# ============================================================

def load_act_datasets():

    print("\nDiscovering Act datasets...")

    discovered = discover_act_datasets()

    all_records = []

    for dataset in discovered:

        act_name = dataset["act_name"]
        file_path = dataset["file_path"]

        print(
            f"\nAct: {act_name}"
        )

        records = load_jsonl(file_path)

        print(
            f"Records: {len(records)}"
        )

        all_records.extend(records)

    print(
        f"\nTotal Act records loaded: "
        f"{len(all_records)}"
    )

    return all_records


# ============================================================
# LOAD COMPLETE LEGAL KNOWLEDGE BASE
# ============================================================

def load_all_legal_records():

    print("=" * 60)
    print("LEGAL AID PROVIDER - DATASET MANAGER")
    print("=" * 60)

    core_records = load_core_dataset()

    act_records = load_act_datasets()

    all_records = (
        core_records +
        act_records
    )

    print("\n" + "=" * 60)

    print(
        f"Core records : {len(core_records)}"
    )

    print(
        f"Act records  : {len(act_records)}"
    )

    print(
        f"Total records: {len(all_records)}"
    )

    print("=" * 60)

    return all_records


# ============================================================
# VALIDATE UNIQUE IDs
# ============================================================

def validate_ids(records):

    ids = []
    duplicate_ids = []

    for record in records:

        record_id = record.get("id")

        if not record_id:
            continue

        if record_id in ids:

            duplicate_ids.append(
                record_id
            )

        ids.append(record_id)

    print(
        f"\nUnique IDs: "
        f"{len(set(ids))}"
    )

    if duplicate_ids:

        print(
            "WARNING: Duplicate IDs found:"
        )

        for duplicate in duplicate_ids:
            print(
                f"  - {duplicate}"
            )

        return False

    print("ID validation: PASSED")

    return True


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    records = load_all_legal_records()

    validate_ids(records)