from week1_pdf_extraction import extract_text_from_pdf
from week1_doc_extraction import extract_text_from_docs


def clean_text(text):
    cleaned_lines = []

    for line in text.splitlines():
        line = " ".join(line.split())

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# DOCX file
raw = extract_text_from_docs("src/data/sample_cvs/report.docx")

# Agar PDF use karni ho to:
# raw = extract_text_from_pdf("src/data/sample_cvs/notes.pdf")

cleaned = clean_text(raw)

print(cleaned)