# Document-Based FAQ Assistant (Fresher Project)

A small local web app that answers questions by finding relevant passages in a folder of documents. It uses TF-IDF and cosine similarity for retrieval, then displays the original passage and filename as evidence. It does not call an external AI service or make up a generated answer.

## What you will learn

- Python functions, modules, files, and error handling
- Flask routes, HTML forms, templates, and static assets
- Basic information retrieval: TF-IDF vectors and cosine similarity
- Showing evidence and communicating the limits of an answer
- Virtual environments, pip, and dependency management

## Requirements

- Python 3.10 or newer
- Visual Studio Code (recommended)
- Internet access once to install Python packages

### VS Code extensions

Install these from the Extensions panel:

1. **Python** by Microsoft — Python language support and interpreter selection.
2. **Pylance** by Microsoft — completions, type checking, and navigation for Python.
3. **Jinja** (optional) — syntax highlighting for Flask's `{{ ... }}` and `{% ... %}` template syntax.

No browser extension is needed. You can use Chrome, Edge, or Firefox.

## Run it

Open the extracted `document-faq-assistant` folder in VS Code. Open a terminal in that folder and run:

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, run the commands without activation using `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe app.py`.

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open the local address shown in the terminal (usually http://127.0.0.1:5000). Ask: **How long can I borrow a book?** or **When is the library open on Saturday?** Stop the server with Ctrl+C.

## Add your own documents

Put plain text `.txt` or Markdown `.md` files in `knowledge_base/`. Separate distinct topics with a blank line; the app treats each paragraph as a searchable passage. Restart the app after editing documents. This starter intentionally supports text/Markdown only; PDF parsing and file uploads are good extensions to implement later.

## How it works

1. A Flask route receives the question from the HTML form.
2. `load_passages()` reads supported files from `knowledge_base/` and splits them into paragraphs.
3. `TfidfVectorizer` represents each paragraph and the question as weighted word/phrase vectors. Common English stop words are removed; one- and two-word phrases are included.
4. Cosine similarity measures how close the question vector is to each paragraph vector.
5. The best three passages above a minimum score are returned with their source filenames. If nothing passes the threshold, the app says it could not find a relevant passage.
6. Jinja renders the answer and citations into the web page.

## Project structure

```text
document-faq-assistant/
├── app.py                    # Flask app and retrieval logic
├── requirements.txt          # Python packages
├── knowledge_base/
│   └── student_handbook.md   # Example source document
├── templates/
│   └── index.html            # Question form and results
└── static/
    └── style.css             # Page styling
```

## Resume description

**Document-Based FAQ Assistant | Python, Flask, scikit-learn, HTML, CSS**  
Built a local web app that searches Markdown and text documents using TF-IDF and cosine similarity, ranks relevant passages, and displays source citations. Added a no-match response and a responsive interface.

Only list features you have run, understood, and can explain. To make it stronger, add tests, PDF ingestion, document upload with validation, chunking for long documents, and a comparison of retrieval approaches. For a later AI extension, use a language model to summarize retrieved passages while requiring citations and preserving the source-based fallback.

## Limits and safe use

This is a learning demo, not a production system. It searches word overlap, so it may miss paraphrases or rank a passage incorrectly. Treat the match percentage as a ranking hint, not a calibrated probability. Do not put private or sensitive documents into a public deployment. Flask's development server is for local learning; production needs a proper WSGI server, security review, and input/resource limits.
