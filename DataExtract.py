import PyPDF2

# Path to your PDF
pdf_path = "C:\\Users\\SOPNIL LAXUMAN\\OneDrive\\Desktop\\Project\\Data\\Bharatiya Nyaya Sanhita.pdf"

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
with open("bns_raw.txt", "w", encoding="utf-8") as output_file:
    output_file.write(full_text)

print("Extraction complete!")
print("File saved as bns_raw.txt")
