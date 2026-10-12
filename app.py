from pathlib import Path

from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"
ALLOWED_EXTENSIONS = {".txt", ".md"}
MIN_SCORE = 0.08

app = Flask(__name__)


def load_passages():
    """Read supported files and split them into paragraph-sized passages."""
    passages = []
    for path in sorted(KNOWLEDGE_DIR.iterdir()):
        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for paragraph in text.split("\n\n"):
                paragraph = " ".join(paragraph.split())
                if paragraph:
                    passages.append({"source": path.name, "text": paragraph})
    return passages


def find_answer(question):
    passages = load_passages()
    if not passages:
        return None, []

    # TF-IDF turns each passage and the question into weighted word vectors.
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        matrix = vectorizer.fit_transform([p["text"] for p in passages] + [question])
    except ValueError:  # e.g. the documents contain no indexable words
        return None, []

    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    best_indices = scores.argsort()[::-1][:3]
    matches = [
        {**passages[i], "score": float(scores[i])}
        for i in best_indices
        if scores[i] >= MIN_SCORE
    ]
    if not matches:
        return "I couldn't find a relevant answer in the documents. Try rephrasing your question or adding a document about that topic.", []

    # This starter retrieves and cites relevant text; it does not invent a summary.
    answer = "Here are the most relevant passages I found in your documents:"
    return answer, matches


@app.route("/", methods=["GET", "POST"])
def home():
    answer = None
    sources = []
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            answer, sources = find_answer(question)
    return render_template("index.html", question=question, answer=answer, sources=sources)


if __name__ == "__main__":
    app.run(debug=True)
