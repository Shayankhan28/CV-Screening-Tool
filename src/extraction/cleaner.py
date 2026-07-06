from src.extraction.week1_pdf_extraction import extract_text_from_pdf
from src.extraction.week1_doc_extraction import extract_text_from_docs


def clean_text(text):
    """Extra whitespace aur blank lines hata kar text ko normalize karta hai."""
    cleaned_lines = []

    for line in text.splitlines():
        line = " ".join(line.split())

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# if __name__ == "__main__":
#     # DOCX file
#     raw = extract_text_from_docs("src/data/sample_cvs/report.docx")

#     # Agar PDF use karni ho to:
#     raw = extract_text_from_pdf("src/data/sample_cvs/notes.pdf")

#     cleaned = clean_text(raw)
#     print(cleaned)