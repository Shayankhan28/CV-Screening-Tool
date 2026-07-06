from docx import Document

def extract_text_from_docs(file_path):
    try:

        doc = Document(file_path)
        all_text = ""
        for data in doc.paragraphs:
            all_text = all_text + data.text + "\n"  
        return all_text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""



# if __name__ == "__main__":
#     result = extract_text_from_docs("src/data/sample_cvs/report.docx")
#     print(result)