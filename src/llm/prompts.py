def build_analysis_prompt(cv_text, job_description):
    prompt = f"""
You are a strict, detail-oriented CV screening assistant. Your job is to compare a candidate's CV against a job description and return a structured, honest analysis.

Job Description:
{job_description}

CV Text:
{cv_text}

Instructions:
- Only use information that is explicitly present in the CV text. Do not guess or invent details.
- "matched_skills": skills/technologies mentioned in the CV that are also relevant to the job description.
- "missing_skills": important skills from the job description that are NOT found anywhere in the CV.
- "years_of_experience": total relevant work experience in years, as a number. Use 0 if not mentioned.
- "education": the highest degree or institution mentioned. Use "Not mentioned" if absent.
- "score": an integer from 0 to 100 representing how well this CV matches the job description overall.
    - 80-100: excellent match, most required skills present
    - 50-79: partial match, some relevant skills present
    - 20-49: weak match, few relevant skills
    - 0-19: little to no relevance
- Do not default the score to 0 unless the CV is genuinely irrelevant to the job description.

Return ONLY valid JSON in exactly this format, with no extra text, no explanation, and no markdown code fences before or after:
{{
    "name": "candidate name or Unknown",
    "summary": "max 3 line summary",
    "matched_skills": ["skill1", "skill2"],
    "missing_skills": ["skill1", "skill2"],
    "years_of_experience": 0,
    "education": "highest degree/institution",
    "score": 0
}}
"""
    return prompt


if __name__ == "__main__":
    from src.llm.ollama_client import ask_ollama
    from src.llm.json_validator import parse_llm_response
    from src.extraction.week1_pdf_extraction import extract_text_from_pdf

    job_description = "Looking for a Python developer with machine learning experience"
    cv_text = extract_text_from_pdf("src/data/sample_cvs/MY CV.pdf")
    prompt = build_analysis_prompt(cv_text, job_description)
    result = ask_ollama(prompt)

    parsed = parse_llm_response(result)
    print(parsed)