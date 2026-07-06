import json


def extract_json_substring(text):
    """Text me se pehla { dhoondta hai. Agar aakhri } mile to wahan tak, warna text ke end tak."""
    start = text.find("{")
    if start == -1:
        return None

    end = text.rfind("}")
    if end == -1 or end < start:
        # Closing brace nahi mila - jo bhi text bacha hai, uska baaki hissa le lo
        return text[start:]

    return text[start:end + 1]


def parse_llm_response(raw_text):
    # Koshish 1: seedha poora text parse karo
    try:
        return json.loads(raw_text)
    except Exception:
        pass

    # Koshish 2: sirf { } ke beech ka hissa nikal kar parse karo
    json_part = extract_json_substring(raw_text)
    if json_part:
        try:
            return json.loads(json_part)
        except Exception:
            pass

        # Koshish 3: agar closing } missing hai, khud jodh k try karo
        try:
            repaired = json_part.rstrip()
            if not repaired.endswith("}"):
                repaired += "}"
            return json.loads(repaired)
        except Exception as e:
            print(f"Failed to parse extracted JSON even after repair: {e}")

    # Sab koshishein fail hoin - safe fallback return karo
    print("Failed to parse LLM response as JSON")
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