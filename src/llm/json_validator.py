import json
import re


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


def strip_comments(text):
    """
    Line-by-line jaata hai aur agar # ya // kisi string ke BAHAR mile (matlab
    quotes ke andar nahi), to us point se lekar line ke end tak hata deta hai.
    """
    cleaned_lines = []

    for line in text.split("\n"):
        in_string = False
        cut_at = None

        for i, ch in enumerate(line):
            if ch == '"' and (i == 0 or line[i - 1] != "\\"):
                in_string = not in_string

            if not in_string:
                if ch == "#":
                    cut_at = i
                    break
                if ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
                    cut_at = i
                    break

        if cut_at is not None:
            line = line[:cut_at]

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def remove_trailing_commas(text):
    """Removes trailing commas before } or ] - e.g. ["a", "b",] -> ["a", "b"]"""
    text = re.sub(r",\s*}", "}", text)
    text = re.sub(r",\s*]", "]", text)
    return text


def parse_llm_response(raw_text):
    # Koshish 1: seedha poora text parse karo
    try:
        return json.loads(raw_text)
    except Exception:
        pass

    # Koshish 2: { } ke beech ka hissa nikalo, comments/trailing-commas saaf karo, phir parse karo
    json_part = extract_json_substring(raw_text)
    if json_part:
        cleaned = strip_comments(json_part)
        cleaned = remove_trailing_commas(cleaned)

        try:
            return json.loads(cleaned)
        except Exception:
            pass

        # Koshish 3: agar closing } missing hai (truncated response), khud jodh k try karo
        try:
            repaired = cleaned.rstrip()
            if not repaired.endswith("}"):
                repaired = remove_trailing_commas(repaired)
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