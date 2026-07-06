import json

def parse_llm_response(raw_text):
    try:
        return json.loads(raw_text)
    except Exception as e:
        print(f"Failed to parse LLM response as JSON: {e}")
        return {
            "name": "PARSE_ERROR",
            "summary": "Could not parse LLM response",
            "matched_skills": [],
            "missing_skills": [],
            "years_of_experience": 0,
            "education": "Unknown",
            "score": 0,
            "raw_response": raw_text
        }