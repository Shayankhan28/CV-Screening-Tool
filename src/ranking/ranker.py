import os
import pandas as pd
from sentence_transformers.util import cos_sim
from src.ranking.embeddings import get_embedding


def get_score(item):
    return item[1]


def rank_cvs(job_description, cv_texts):
    jd_embedding = get_embedding(job_description)
    results = []

    for filename, text in cv_texts.items():
        cv_embedding = get_embedding(text)
        score = cos_sim(jd_embedding, cv_embedding)
        results.append((filename, float(score)))

    return sorted(results, key=get_score, reverse=True)


def make_results_table(ranked_cvs):
    df = pd.DataFrame(ranked_cvs, columns=["Filename", "Score"])
    return df


if __name__ == "__main__":
    from src.extraction.week1_pdf_extraction import extract_text_from_pdf
    from src.extraction.week1_doc_extraction import extract_text_from_docs

    # project root folder ka path nikalna (src ke ek level upar)
    project_root = os.path.dirname(os.path.dirname(__file__))
    cv_folder = os.path.join(project_root, "data", "sample_cvs")

    job_description = "Looking for a Python developer with machine learning experience"

    # sample_cvs folder ki har file padho aur text nikalo
    cv_texts = {}
    for filename in os.listdir(cv_folder):
        path = os.path.join(cv_folder, filename)

        if filename.endswith(".pdf"):
            cv_texts[filename] = extract_text_from_pdf(path)
        elif filename.endswith(".docx"):
            cv_texts[filename] = extract_text_from_docs(path)

    ranked = rank_cvs(job_description, cv_texts)

    results_df = make_results_table(ranked)
    print("\nRanked CVs:\n")
    print(results_df)