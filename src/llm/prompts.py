def build_analysis_prompt(cv_text, job_description):
    prompt = f"""
You are a strict, detail-oriented CV screening assistant. Your job is to compare a candidate's CV against a job description and return a structured, honest analysis.

Job Description:
{job_description}

CV Text:
{cv_text}

CRITICAL RULE - READ CAREFULLY:
- You must treat the "Job Description" text above as the ONLY source of truth for what skills are required.
- Do NOT use your own general knowledge of what this job title "usually" requires.
- Do NOT assume a "Python Developer" needs HTML/CSS/JavaScript/React/SQL/etc unless those words are ACTUALLY written in the Job Description above.
- If the Job Description is short, vague, or just a job title with no explicit skill list, then you must NOT invent skills for it. In that case, "missing_skills" should be an empty list [].
- Only mention a skill in "missing_skills" if it is LITERALLY written or clearly named in the Job Description text, and is NOT present in the CV.

Instructions:
- Only use information that is explicitly present in the CV text. Do not guess or invent details.
- "matched_skills": skills/technologies that are explicitly written in the Job Description AND are also found in the CV.
- "missing_skills": skills/technologies that are explicitly written in the Job Description but are NOT found anywhere in the CV. Never add a skill here that isn't literally mentioned in the Job Description text.
- "years_of_experience": total relevant work experience in years, as a number. Use 0 if not mentioned.
- "education": the highest degree or institution mentioned. Use "Not mentioned" if absent.
- "score": an integer from 0 to 100 representing how well this CV matches the job description overall.
    - 80-100: excellent match, most required skills present
    - 50-79: partial match, some relevant skills present
    - 20-49: weak match, few relevant skills
    - 0-19: little to no relevance
- Do not default the score to 0 unless the CV is genuinely irrelevant to the job description.

Before answering, silently double-check: every entry in "missing_skills" must actually appear as text in the Job Description above. If it doesn't appear there, remove it.

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