import fitz

def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        all_text = ""
        for page in doc:
            all_text = all_text + page.get_text()
        return all_text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""


if __name__ == "__main__":
    result = extract_text_from_pdf("src/data/sample_cvs/notes.pdf")
    print(result)