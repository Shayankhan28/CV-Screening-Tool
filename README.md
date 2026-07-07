# CV Screening Tool

A fully local, zero-cost AI-powered CV screening assistant for Adivantech's hiring process.
Reads a folder/batch of CVs (PDF and DOCX), ranks them against a job description using
local embeddings, and produces an AI-analyzed shortlist exported to Excel.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- A pulled local model (e.g. `llama3.2:3b` or `phi3:mini`)

## Setup (from scratch on a new PC)

1. Clone the repo:
```bash
   git clone <repo-url>
   cd CV-Screening-Tool
```

2. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Install Ollama and pull a model:
```bash
   ollama pull llama3.2:3b
```
   (or `ollama pull phi3:mini` — update the model name in `src/llm/ollama_client.py` if you switch)

5. Run the app:
```bash
   streamlit run src/ui/app.py
```

6. Open `http://localhost:8501` in your browser.

## How to use

1. Paste the job description (write 2-3 full sentences with required skills, not just a single keyword).
2. Upload CVs (PDF/DOCX, multiple files allowed).
3. Choose how many top candidates you want the AI to analyze in detail.
4. Click **Scan CVs**.
5. Review the ranked table and download the Excel export.

## Notes

- Everything runs 100% locally — no candidate data leaves the machine, no internet needed after setup.
- Scanned/image-only PDFs will not extract text and will be flagged for manual review.