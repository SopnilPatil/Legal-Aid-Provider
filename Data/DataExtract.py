import os
from pathlib import Path
import PyPDF2

# Path to PDF relative to script directory
BASE_DIR = Path(__file__).resolve().parent
pdf_path = BASE_DIR / "Indian Constitution" / "Indian constitution.pdf"
if not pdf_path.exists():
    pdf_path = BASE_DIR / "Constitution of India.pdf"

# Open the PDF file
with open(pdf_path, "rb") as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    full_text = ""

    # Loop through all pages
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()
        if text:
            full_text += text + "\n"

# Save extracted text to a file
with open("IndianConstitutionRaw.txt", "w", encoding="utf-8") as output_file:
    output_file.write(full_text)

print("Extraction complete!")
print("File saved as IndianConstitutionRaw.txt")
