import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import pandas as pd
import tempfile

from src.extraction.week1_pdf_extraction import extract_text_from_pdf
from src.extraction.week1_doc_extraction import extract_text_from_docs
from src.extraction.cleaner import clean_text
from src.ranking.ranker import rank_cvs
from src.llm.ollama_client import ask_ollama
from src.llm.prompts import build_analysis_prompt
from src.llm.json_validator import parse_llm_response


st.title("CV Screening Tool")

job_description = st.text_area("Paste the Job Description here")

uploaded_files = st.file_uploader(
    "Upload CVs (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

top_n = st.number_input("How many top candidates to analyze with AI?", min_value=1, max_value=50, value=5)

if st.button("Scan CVs"):
    if not job_description:
        st.error("Please paste a job description first.")
    elif not uploaded_files:
        st.error("Please upload at least one CV.")
    else:
        with st.spinner("Extracting text from CVs..."):
            cv_texts = {}
            skipped_files = []
            empty_files = []
            temp_dir = tempfile.mkdtemp()

            for uploaded_file in uploaded_files:
                temp_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                lower_name = uploaded_file.name.lower()
                if lower_name.endswith(".pdf"):
                    raw_text = extract_text_from_pdf(temp_path)
                elif lower_name.endswith(".docx"):
                    raw_text = extract_text_from_docs(temp_path)
                else:
                    skipped_files.append(uploaded_file.name)
                    continue

                if not raw_text.strip():
                    empty_files.append(uploaded_file.name)

                cv_texts[uploaded_file.name] = clean_text(raw_text)

            if skipped_files:
                st.warning(f"Skipped unsupported files: {', '.join(skipped_files)}")
            if empty_files:
                st.warning(
                    f"No text could be extracted from: {', '.join(empty_files)} "
                    "(file may be corrupt, empty, or a scanned image)."
                )

        if not cv_texts:
            st.error("No readable CVs found in the uploaded files. Please check the files and try again.")
            st.stop()

        with st.spinner("Ranking CVs against job description..."):
            ranked = rank_cvs(job_description, cv_texts)

        final_results = []
        progress_bar = st.progress(0)

        for i, (filename, similarity_score) in enumerate(ranked[:top_n]):
            with st.spinner(f"Analyzing {filename} with AI ({i+1}/{top_n})..."):
                cv_text = cv_texts[filename]
                prompt = build_analysis_prompt(cv_text, job_description)
                raw_response = ask_ollama(prompt)
                analysis = parse_llm_response(raw_response)

                analysis["filename"] = filename
                analysis["similarity_score"] = round(similarity_score, 4)
                final_results.append(analysis)

            progress_bar.progress((i + 1) / top_n)

        st.success("Screening complete!")

        results_df = pd.DataFrame(final_results)
        st.dataframe(results_df)