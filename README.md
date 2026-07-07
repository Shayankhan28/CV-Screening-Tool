# CV Screening Tool

**AI-Powered CV / Resume Screening Tool — Adivantech Internal Project (ADV-AI-001)**

A fully local, zero-cost candidate shortlisting assistant. It reads a batch of CVs (PDF and DOCX),
ranks them against a job description using local embeddings, generates a structured AI analysis
for the top candidates, and exports the final shortlist to Excel — entirely offline, with no
candidate data ever leaving the machine.

> This tool assists initial screening only. A human recruiter always makes the final hiring decision.

---

## Features

- 📂 Bulk upload of CVs in PDF and DOCX format
- 🧠 Local embedding-based ranking (sentence-transformers) against a pasted job description
- 🤖 Local LLM analysis via Ollama — summary, matched/missing skills, experience, education, score
- 📊 Sortable results table in a Streamlit web interface
- 📥 One-click Excel export of the full ranked shortlist
- ⚠️ Automatic flagging of corrupt, unsupported, or scanned/image-only CVs for manual review
- 🔒 100% local and offline — zero cloud calls, zero recurring cost

---

## Tech Stack

| Component            | Tool / Library                          |
|-----------------------|------------------------------------------|
| Language               | Python 3.10+                            |
| Local LLM runtime      | [Ollama](https://ollama.com)             |
| Model                  | `phi3:mini` (default)                   |
| CV text extraction     | PyMuPDF (`fitz`), `python-docx`, with `pdfplumber` as fallback |
| Ranking / embeddings   | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Interface              | Streamlit                               |
| Data / export          | `pandas`, `openpyxl`                    |

---

## Requirements

- Python 3.10 or higher
- [Ollama](https://ollama.com) installed and running locally
- At least one local model pulled (`phi3:mini` recommended; `llama3.2:3b` also supported)

---

## Setup (from scratch on a new PC)

1. **Clone the repository**
```bash
   git clone <repo-url>
   cd CV-Screening-Tool
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Install Ollama and pull the model**
```bash
   ollama pull phi3:mini
```
   To use a different model instead, pull it (e.g. `ollama pull llama3.2:3b`) and update the
   `model` value in `src/llm/ollama_client.py` accordingly.

5. **Run the app**
```bash
   streamlit run src/ui/app.py
```

6. **Open the app** at [http://localhost:8501](http://localhost:8501)

---

## How to Use

1. Paste the job description — write 2–3 full sentences describing the role and required
   skills (a single keyword like *"JavaScript"* gives the ranking model too little signal
   to work with).
2. Upload one or more CVs (PDF or DOCX).
3. Choose how many top-ranked candidates the AI should analyze in detail.
4. Click **Scan CVs**.
5. Review the ranked, analyzed results table and download it as an Excel file.

---

## Project Structure


---

## Notes & Limitations

- Everything runs 100% locally — no internet connection or external API calls are made
  after initial setup.
- Scanned or image-only PDFs currently cannot be read (no OCR yet) and are flagged for
  manual review instead of being silently skipped.
- Model output quality depends on the local LLM chosen; smaller models may occasionally
  produce inconsistent scores on very short or vague job descriptions.