import json
from pathlib import Path
import re



# PROJECT PATHS


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"

OUTPUT_FILE = DATA_DIR / "unified_legal_dataset.jsonl"



# FILE FINDER


def find_file(filename):
    """
    Search the entire Data folder for a specific file.
    """

    matches = list(DATA_DIR.rglob(filename))

    if not matches:
        return None

    return matches[0]



# LOAD JSON


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



# LOAD JSONL

def load_jsonl(path):

    records = []

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1
        ):

            line = line.strip()

            if not line:
                continue

            try:

                records.append(
                    json.loads(line)
                )

            except json.JSONDecodeError as error:

                print(
                    f"⚠️ Invalid JSON:"
                    f" {path.name}"
                    f" line {line_number}"
                )

                print(error)

    return records



# CONSTITUTION NORMALIZER


def normalize_constitution(record, index):

    source_type = record.get(
        "source_type",
        "article"
    )

    
    # Preamble
   
    if source_type == "preamble":

        return {

            "id": record.get(
                "chunk_id",
                f"CONSTITUTION-PREAMBLE-{index}"
            ),

            "text": record.get(
                "text",
                ""
            ),

            "metadata": {

                "law_code": "CONSTITUTION",

                "law_name":
                    "Constitution of India",

                "provision_type":
                    "preamble",

                "part_number": None,

                "part_title": None,

                "chapter_number": None,

                "chapter_title": None,

                "provision_number":
                    "Preamble",

                "provision_title":
                    "Preamble",

                "source_document":
                    record.get(
                        "source",
                        {}
                    ).get(
                        "file",
                        "Indian constitution.pdf"
                    ),

                "source_pages": [
                    record.get(
                        "source",
                        {}
                    ).get(
                        "source_page"
                    )
                ]
            }
        }


    
    # Article
    


def normalize_constitution(record, index):

    chunk_id = record.get(
        "chunk_id",
        ""
    )

    source_type = record.get(
        "source_type",
        ""
    )

    
    # PREAMBLE
    
    if source_type == "preamble" or "PREAMBLE" in chunk_id:

        source = record.get(
            "source",
            {}
        )

        return {

            "id": record.get(
                "chunk_id",
                f"CONSTITUTION-PREAMBLE-{index}"
            ),

            "text": record.get(
                "text",
                ""
            ),

            "metadata": {

                "law_code":
                    "CONSTITUTION",

                "law_name":
                    "Constitution of India",

                "provision_type":
                    "preamble",

                "part_number":
                    None,

                "part_title":
                    None,

                "chapter_number":
                    None,

                "chapter_title":
                    None,

                "provision_number":
                    "Preamble",

                "provision_title":
                    "Preamble",

                "source_document":
                    source.get(
                        "file",
                        "Indian constitution.pdf"
                    ),

                "source_pages": [
                    source.get(
                        "source_page"
                    )
                ]
            }
        }


    
    # SCHEDULE
   

    if "SCHEDULE" in chunk_id:

        source = record.get(
            "source",
            {}
        )

        # Extract schedule name from chunk ID
        schedule_part = (
            chunk_id
            .replace(
                "CONSTITUTION-",
                ""
            )
            .replace(
                "-CHUNK-001",
                ""
            )
        )

        # Example:
        # FIRST-SCHEDULE
        # SECOND-SCHEDULE

        schedule_name = (
            schedule_part
            .replace(
                "-",
                " "
            )
            .title()
        )

        return {

            "id": record.get(
                "chunk_id",
                f"CONSTITUTION-SCHEDULE-{index}"
            ),

            "text": record.get(
                "text",
                ""
            ),

            "metadata": {

                "law_code":
                    "CONSTITUTION",

                "law_name":
                    "Constitution of India",

                "provision_type":
                    "schedule",

                "part_number":
                    None,

                "part_title":
                    None,

                "chapter_number":
                    None,

                "chapter_title":
                    None,

                "provision_number":
                    schedule_name,

                "provision_title":
                    schedule_name,

                "source_document":
                    source.get(
                        "file",
                        "Indian constitution.pdf"
                    ),

                "source_pages": [
                    source.get(
                        "source_page"
                    )
                ]
            }
        }


    
    # APPENDIX
    

    if "APPENDIX" in chunk_id:

        source = record.get(
            "source",
            {}
        )

        appendix_name = (
            chunk_id
            .replace(
                "CONSTITUTION-",
                ""
            )
            .replace(
                "-CHUNK-001",
                ""
            )
            .replace(
                "-",
                " "
            )
            .title()
        )

        return {

            "id": record.get(
                "chunk_id",
                f"CONSTITUTION-APPENDIX-{index}"
            ),

            "text": record.get(
                "text",
                ""
            ),

            "metadata": {

                "law_code":
                    "CONSTITUTION",

                "law_name":
                    "Constitution of India",

                "provision_type":
                    "appendix",

                "part_number":
                    None,

                "part_title":
                    None,

                "chapter_number":
                    None,

                "chapter_title":
                    None,

                "provision_number":
                    appendix_name,

                "provision_title":
                    appendix_name,

                "source_document":
                    source.get(
                        "file",
                        "Indian constitution.pdf"
                    ),

                "source_pages": [
                    source.get(
                        "source_page"
                    )
                ]
            }
        }


 
    # ARTICLE
    
    part = record.get(
        "part"
    )

    chapter = record.get(
        "chapter"
    )

    return {

        "id": record.get(
            "chunk_id",
            f"CONSTITUTION-{index}"
        ),

        "text": record.get(
            "text",
            ""
        ),

        "metadata": {

            "law_code":
                "CONSTITUTION",

            "law_name":
                "Constitution of India",

            "provision_type":
                "article",

            "part_number":
                part.get("number")
                if isinstance(part, dict)
                else None,

            "part_title":
                part.get("title")
                if isinstance(part, dict)
                else None,

            "chapter_number":
                chapter.get("number")
                if isinstance(chapter, dict)
                else None,

            "chapter_title":
                chapter.get("title")
                if isinstance(chapter, dict)
                else None,

            "provision_number":
                record.get(
                    "article_number"
                ),

            "provision_title":
                record.get(
                    "article_title"
                ),

            "source_document":
                record.get(
                    "source",
                    {}
                ).get(
                    "file",
                    "Indian constitution.pdf"
                ),

            "source_pages": [
                record.get(
                    "source",
                    {}
                ).get(
                    "source_page"
                )
            ]
        }
    }




# BNS NORMALIZER

def normalize_bns(record, index):

    return {

        "id": record.get(
            "id",
            f"BNS-{index}"
        ),

        "text": record.get(
            "text",
            ""
        ),

        "metadata": {

            "law_code":
                "BNS",

            "law_name":
                record.get(
                    "act_name",
                    "Bharatiya Nyaya Sanhita, 2023"
                ),

            "provision_type":
                "section",

            "part_number":
                None,

            "part_title":
                None,

            "chapter_number":
                record.get(
                    "chapter"
                ),

            "chapter_title":
                record.get(
                    "chapter_title"
                ),

            "provision_number":
                record.get(
                    "section"
                ),

            "provision_title":
                record.get(
                    "section_title"
                ),

            "source_document":
                record.get(
                    "source",
                    "BNS.pdf"
                ),

            "source_pages":
                list(
                    range(
                        record.get(
                            "source_page_start",
                            0
                        ),
                        record.get(
                            "source_page_end",
                            record.get(
                                "source_page_start",
                                0
                            )
                        ) + 1
                    )
                )
        }
    }



# BNSS NORMALIZER


def normalize_bnss(record, index):

    metadata = record.get("metadata", {})

    record_id = str(
        record.get("id", "")
    )

    text = record.get(
        "text",
        ""
    )

    
    # BNSS SCHEDULE
   

    if "BNSS-SCHEDULE-" in record_id:

        match = re.search(
            r"BNSS-SCHEDULE-(FIRST|SECOND)-CHUNK-(\d+)",
            record_id,
            re.IGNORECASE
        )

        if match:

            schedule_name = (
                match.group(1).title()
                + " Schedule"
            )

        else:

            schedule_name = "BNSS Schedule"


        return {

            "id": record_id,

            "text": text,

            "metadata": {

                "law_code":
                    "BNSS",

                "law_name":
                    record.get(
                        "act_name",
                        "Bharatiya Nagarik Suraksha Sanhita, 2023"
                    ),

                "provision_type":
                    "schedule",

                "part_number":
                    None,

                "part_title":
                    None,

                "chapter_number":
                    None,

                "chapter_title":
                    None,

                "provision_number":
                    schedule_name,

                "provision_title":
                    schedule_name,

                "source_document":
                    record.get(
                        "source",
                        metadata.get(
                            "source",
                            "BNSS.pdf"
                        )
                    ),

                "source_pages":
                    []
            }
        }


    
    # BNSS SECTION
    
    section_number = record.get(
        "section"
    )

    if section_number is None:

        section_number = metadata.get(
            "section"
        )


    
    # Extract section number from ID
   
    if section_number is None:

        match = re.search(
            r"BNSS-SEC-(\d+)",
            record_id,
            re.IGNORECASE
        )

        if match:

            section_number = match.group(1)


    
    # SECTION TITLE
   

    section_title = record.get(
        "section_title"
    )

    if not section_title:

        section_title = metadata.get(
            "section_title"
        )


    
    # CHAPTER
    

    chapter_number = record.get(
        "chapter"
    )

    if chapter_number is None:

        chapter_number = metadata.get(
            "chapter"
        )


    chapter_title = record.get(
        "chapter_title"
    )

    if not chapter_title:

        chapter_title = metadata.get(
            "chapter_title"
        )


    
    # SOURCE
    

    source = record.get(
        "source"
    )

    if not source:

        source = metadata.get(
            "source",
            "BNSS.pdf"
        )


   
    # SOURCE PAGES
    

    page_start = record.get(
        "source_page_start"
    )

    if page_start is None:

        page_start = metadata.get(
            "source_page_start"
        )


    page_end = record.get(
        "source_page_end"
    )

    if page_end is None:

        page_end = metadata.get(
            "source_page_end"
        )


    source_pages = []


    if page_start is not None:

        if page_end is None:

            page_end = page_start

        source_pages = list(
            range(
                int(page_start),
                int(page_end) + 1
            )
        )


    
    # RETURN SECTION
    
    return {

        "id": record_id
        if record_id
        else f"BNSS-{index}",

        "text": text,

        "metadata": {

            "law_code":
                "BNSS",

            "law_name":
                record.get(
                    "act_name",
                    metadata.get(
                        "act_name",
                        "Bharatiya Nagarik Suraksha Sanhita, 2023"
                    )
                ),

            "provision_type":
                "section",

            "part_number":
                None,

            "part_title":
                None,

            "chapter_number":
                chapter_number,

            "chapter_title":
                chapter_title,

            "provision_number":
                section_number,

            "provision_title":
                section_title,

            "source_document":
                source,

            "source_pages":
                source_pages
        }
    }



# VALIDATE RECORD

def valid_record(record):

    if not isinstance(
        record,
        dict
    ):
        return False

    text = record.get(
        "text",
        ""
    )

    if not isinstance(
        text,
        str
    ):
        return False

    if not text.strip():
        return False

    return True



# MAIN


def main():

    print("=" * 60)
    print("UNIFIED LEGAL DATASET BUILDER")
    print("=" * 60)


    unified_data = []


   
    # FIND FILES
   
    constitution_file = find_file(
        "constitution_search_chunks.json"
    )

    bns_file = find_file(
        "bns_rag.jsonl"
    )

    bnss_file = find_file(
        "bnss_rag.jsonl"
    )


    
    # SHOW FILES
    

    print("\n📂 DATASET FILES")


    if constitution_file:

        print(
            "✅ Constitution:"
        )

        print(
            f"   {constitution_file}"
        )

    else:

        print(
            "❌ Constitution dataset not found"
        )


    if bns_file:

        print(
            "✅ BNS:"
        )

        print(
            f"   {bns_file}"
        )

    else:

        print(
            "❌ BNS dataset not found"
        )


    if bnss_file:

        print(
            "✅ BNSS:"
        )

        print(
            f"   {bnss_file}"
        )


  
    # CONSTITUTION
   
    if constitution_file:

        print(
            "\n📚 Loading Constitution..."
        )

        constitution_data = load_json(
            constitution_file
        )

        print(
            f"   Found {len(constitution_data)} records"
        )

        for index, record in enumerate(
            constitution_data
        ):

            normalized = normalize_constitution(
                record,
                index
            )

            if valid_record(
                normalized
            ):

                unified_data.append(
                    normalized
                )


    # BNS
    

    if bns_file:

        print(
            "\n⚖️ Loading BNS..."
        )

        bns_data = load_jsonl(
            bns_file
        )

        print(
            f"   Found {len(bns_data)} records"
        )

        for index, record in enumerate(
            bns_data
        ):

            normalized = normalize_bns(
                record,
                index
            )

            if valid_record(
                normalized
            ):

                unified_data.append(
                    normalized
                )


    
    # BNSS
    

    if bnss_file:

        print(
            "\n⚖️ Loading BNSS..."
        )

        bnss_data = load_jsonl(
            bnss_file
        )

        print(
            f"   Found {len(bnss_data)} records"
        )

        for index, record in enumerate(
            bnss_data
        ):

            normalized = normalize_bnss(
                record,
                index
            )

            if valid_record(
                normalized
            ):

                unified_data.append(
                    normalized
                )


    
    # SAVE
    

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        for record in unified_data:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
                + "\n"
            )


    
    # COUNTS
    

    constitution_count = 0
    bns_count = 0
    bnss_count = 0


    for record in unified_data:

        code = record[
            "metadata"
        ][
            "law_code"
        ]

        if code == "CONSTITUTION":

            constitution_count += 1

        elif code == "BNS":

            bns_count += 1

        elif code == "BNSS":

            bnss_count += 1


    
    # RESULT
    

    print("\n" + "=" * 60)
    print("✅ UNIFIED DATASET CREATED")
    print("=" * 60)

    print(
        f"\nConstitution : {constitution_count}"
    )

    print(
        f"BNS          : {bns_count}"
    )

    print(
        f"BNSS         : {bnss_count}"
    )

    print(
        f"Total        : {len(unified_data)}"
    )

    print(
        "\nOutput:"
    )

    print(
        OUTPUT_FILE
    )

    print(
        "\nNext step:"
    )

    print(
        "Run validate_data.py"
    )


if __name__ == "__main__":

    main()