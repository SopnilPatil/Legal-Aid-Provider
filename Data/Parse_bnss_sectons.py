import re
import json
from pathlib import Path

# Read raw text
BASE_DIR = Path(__file__).resolve().parent
raw_file = BASE_DIR / "bnss_raw.txt"
with open(raw_file, "r", encoding="utf-8") as f:
    text = f.read()

# Normalize whitespace
text = re.sub(r'\s+', ' ', text)

# Detect chapter headings
chapter_pattern = r'(CHAPTER\s+[IVXLC]+\s*[^C]*?)'
chapters = re.split(chapter_pattern, text)

data = []
current_chapter = "Unknown"

for part in chapters:

    # If chapter heading
    if re.match(r'CHAPTER\s+[IVXLC]+', part):
        current_chapter = part.strip()
        continue

    # Detect sections like "Section 1" OR "1."
    section_pattern = r'(Section\s+\d+[A-Z]?|\b\d+\.)'
    sections = re.split(section_pattern, part)

    for i in range(1, len(sections), 2):

        section_number = sections[i].strip()
        section_content = sections[i+1].strip() if i+1 < len(sections) else ""

        data.append({
            "law": "BNSS",
            "chapter": current_chapter,
            "section": section_number,
            "content": section_content
        })

# Save JSON
with open("bnss_structured.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("BNSS parsing finished")
print("Total sections extracted:", len(data))