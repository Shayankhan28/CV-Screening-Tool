import os
from src.extraction.week1_pdf_extraction import extract_text_from_pdf
from src.extraction.week1_doc_extraction import extract_text_from_docs
from src.extraction.cleaner import clean_text
from src.ranking.ranker import rank_cvs
from src.llm.ollama_client import ask_ollama
from src.llm.prompts import build_analysis_prompt
from src.llm.json_validator import parse_llm_response


def load_cv_text(cv_folder):
    cv_text = {}
    skipped_files = []

    for filename in os.listdir(cv_folder):
        path = os.path.join(cv_folder, filename)
        lower_name = filename.lower()

        if lower_name.endswith(".pdf"):
            raw_text = extract_text_from_pdf(path)
        elif lower_name.endswith(".docx"):
            raw_text = extract_text_from_docs(path)
        else:
            skipped_files.append(filename)
            continue

        if not raw_text.strip():
            print(f"Warning: no text extracted from {filename} (corrupt/empty/scanned file?)")

        cv_text[filename] = clean_text(raw_text)

    if skipped_files:
        print(f"Skipped unsupported files: {skipped_files}")

    return cv_text


def run_pipeline(cv_folder, job_description, top_n=10):

    all_cv_texts = load_cv_text(cv_folder)
    ranked = rank_cvs(job_description, all_cv_texts)

    final_results = []
    for filename, similarity_score in ranked[:top_n]:
        cv_text = all_cv_texts[filename]
        prompt = build_analysis_prompt(cv_text, job_description)
        raw_response = ask_ollama(prompt)
        analysis = parse_llm_response(raw_response)

        analysis["filename"] = filename
        analysis["similarity_score"] = similarity_score
        final_results.append(analysis)

    return final_results

if __name__ == "__main__":
    cv_folder = "src/data/sample_cvs"
    job_description = "Looking for a Python developer with machine learning experience"

    results = run_pipeline(cv_folder, job_description, top_n=5)

    for r in results:
        print(r)
        print("---")