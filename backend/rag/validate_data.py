import json
from pathlib import Path
from collections import Counter



# PATH


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    BASE_DIR
    / "Data"
    / "unified_legal_dataset.jsonl"
)



# REQUIRED METADATA


REQUIRED_METADATA = [
    "law_code",
    "law_name",
    "provision_type",
    "source_document",
]



# MAIN

def main():

    print("=" * 60)
    print("LEGAL DATASET QUALITY CHECK")
    print("=" * 60)


    
    # CHECK FILE
    

    if not DATASET_FILE.exists():

        print("\n❌ Dataset not found:")
        print(DATASET_FILE)

        return


   
    # LOAD DATA
    

    records = []

    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1
        ):

            if not line.strip():
                continue

            try:

                records.append(
                    json.loads(line)
                )

            except json.JSONDecodeError as error:

                print(
                    f"❌ Invalid JSON at line "
                    f"{line_number}: {error}"
                )


    print(
        f"\n📄 Total records: {len(records)}"
    )


    
    # LEGAL SOURCE COUNTS
    

    law_counter = Counter()

    for record in records:

        metadata = record.get(
            "metadata",
            {}
        )

        law_code = metadata.get(
            "law_code",
            "UNKNOWN"
        )

        law_counter[law_code] += 1


    print(
        "\n📚 Records by legal source:"
    )

    for law, count in law_counter.items():

        print(
            f"   {law:<15} : {count}"
        )


    
    # MISSING TEXT
   

    missing_text = []

    for index, record in enumerate(records):

        text = record.get(
            "text",
            ""
        )

        if (
            not isinstance(text, str)
            or not text.strip()
        ):

            missing_text.append(
                index + 1
            )


    print(
        f"\n📝 Missing text: "
        f"{len(missing_text)}"
    )


    
    # PROVISION TYPES
    

    type_counter = Counter()

    for record in records:

        metadata = record.get(
            "metadata",
            {}
        )

        provision_type = metadata.get(
            "provision_type",
            "UNKNOWN"
        )

        type_counter[provision_type] += 1


    print(
        "\n📑 Provision types:"
    )

    for provision_type, count in (
        type_counter.most_common()
    ):

        print(
            f"   {provision_type:<20} : {count}"
        )


    
    # METADATA VALIDATION
    

    missing_records = []

    missing_field_counter = Counter()


    for index, record in enumerate(records):

        metadata = record.get(
            "metadata",
            {}
        )

        missing_fields = []


       
        # Basic metadata
        

        for field in REQUIRED_METADATA:

            value = metadata.get(
                field
            )

            if (
                value is None
                or value == ""
                or value == []
            ):

                missing_fields.append(
                    field
                )

                missing_field_counter[
                    field
                ] += 1


        
        # Article / Section validation
       

        provision_type = metadata.get(
            "provision_type"
        )

        if provision_type in [
            "article",
            "section"
        ]:

            number = metadata.get(
                "provision_number"
            )

            title = metadata.get(
                "provision_title"
            )


            if (
                number is None
                or number == ""
            ):

                missing_fields.append(
                    "provision_number"
                )

                missing_field_counter[
                    "provision_number"
                ] += 1


            if (
                title is None
                or title == ""
            ):

                missing_fields.append(
                    "provision_title"
                )

                missing_field_counter[
                    "provision_title"
                ] += 1


       
        # Schedule validation
       

        elif provision_type == "schedule":

            schedule_number = metadata.get(
                "provision_number"
            )

            if (
                schedule_number is None
                or schedule_number == ""
            ):

                missing_fields.append(
                    "schedule_number"
                )

                missing_field_counter[
                    "schedule_number"
                ] += 1


        
        # Preamble
        

        elif provision_type == "preamble":

            # No Article/Section number required.
            pass


        
        # Appendix
        
        elif provision_type == "appendix":

            # Appendix-specific numbering can be
            # handled separately if present.
            pass


       
        # Unknown type
        
        elif provision_type in [
            None,
            "",
            "UNKNOWN"
        ]:

            missing_fields.append(
                "provision_type"
            )


        if missing_fields:

            missing_records.append(
                {
                    "index": index + 1,

                    "id": record.get(
                        "id"
                    ),

                    "law_code":
                        metadata.get(
                            "law_code"
                        ),

                    "provision_type":
                        provision_type,

                    "missing_fields":
                        missing_fields
                }
            )


    print(
        "\n🏷️ Records with metadata issues: "
        f"{len(missing_records)}"
    )


    
    # MISSING FIELD SUMMARY
   

    if missing_field_counter:

        print(
            "\nMissing metadata fields:"
        )

        for field, count in (
            missing_field_counter.most_common()
        ):

            print(
                f"   {field:<20} : {count}"
            )

    else:

        print(
            "\n✅ No required metadata fields are missing."
        )


    
    # SHOW PROBLEMATIC RECORDS
    

    if missing_records:

        print(
            "\n" + "=" * 60
        )

        print(
            "EXAMPLES OF RECORDS WITH METADATA ISSUES"
        )

        print(
            "=" * 60
        )


        for item in missing_records[:10]:

            print(
                f"\nID: {item['id']}"
            )

            print(
                f"Law: {item['law_code']}"
            )

            print(
                f"Type: {item['provision_type']}"
            )

            print(
                "Missing:"
            )

            for field in item[
                "missing_fields"
            ]:

                print(
                    f"   - {field}"
                )


    
    # DUPLICATE IDS
    

    ids = [
        record.get("id")
        for record in records
    ]

    id_counter = Counter(ids)

    duplicate_ids = [
        record_id
        for record_id, count
        in id_counter.items()
        if count > 1
    ]


    print(
        "\n🆔 Duplicate IDs: "
        f"{len(duplicate_ids)}"
    )


    
    # INVALID RECORD OBJECTS
    

    invalid_records = []

    for index, record in enumerate(records):

        if not isinstance(
            record,
            dict
        ):

            invalid_records.append(
                index + 1
            )


    print(
        "📦 Invalid record objects: "
        f"{len(invalid_records)}"
    )


    
    # FINAL RESULT
    
    print(
        "\n" + "=" * 60
    )


    if (
        len(missing_text) == 0
        and len(duplicate_ids) == 0
        and len(invalid_records) == 0
        and len(missing_records) == 0
    ):

        print(
            "✅ DATASET VALIDATION PASSED"
        )

        print(
            "The unified dataset is ready "
            "for the embedding stage."
        )

    else:

        print(
            "⚠️ DATASET NEEDS ATTENTION"
        )

        print(
            f"Metadata issues: "
            f"{len(missing_records)}"
        )


    print(
        "=" * 60
    )



# PROGRAM ENTRY


if __name__ == "__main__":

    main()