import fitz
import pdfplumber

def extract_text_from_pdf(file_path):
    all_text = ""

    # Koshish 1: PyMuPDF (fitz) - fast aur zyada tar cases mein sahi
    try:
        doc = fitz.open(file_path)
        for page in doc:
            all_text = all_text + page.get_text()
    except Exception as e:
        print(f"fitz failed to read {file_path}: {e}")
        all_text = ""

    # Koshish 2: agar fitz se kuch nahi mila, pdfplumber try karo
    if not all_text.strip():
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        all_text = all_text + page_text + "\n"
        except Exception as e:
            print(f"pdfplumber also failed to read {file_path}: {e}")
            all_text = ""

    return all_text


# if __name__ == "__main__":
#     result = extract_text_from_pdf("src/data/sample_cvs/notes.pdf")
#     print(result)