from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import json
import os
import re

app = Flask(__name__, static_folder=".")
CORS(app)

# ── Configure Groq ───────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set")

client = Groq(api_key=GROQ_API_KEY)

# ── Helper: strip markdown fences ────────────────────────────────────────────
def extract_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()

# ── Route: Generate Quiz ─────────────────────────────────────────────────────
@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    data = request.get_json()

    topic      = data.get("topic", "").strip()
    syllabus   = data.get("syllabus", "").strip()
    difficulty = data.get("difficulty", "Medium")

    try:
        num_q = min(max(int(data.get("num_questions", 10)), 1), 20)
    except:
        return jsonify({"error": "Invalid number of questions"}), 400

    if not topic and not syllabus:
        return jsonify({"error": "Provide a topic or syllabus."}), 400

    # Build content descriptor
    if syllabus:
        content_desc = f"based on the following syllabus:\n{syllabus}"
    else:
        content_desc = f"on the topic: {topic}"

    prompt = f"""
You are a quiz generator. Generate exactly {num_q} multiple-choice questions {content_desc}.
Difficulty level: {difficulty}.

Return ONLY raw JSON.
Do NOT use markdown.
Do NOT include explanation outside JSON.

Format:
[
  {{
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "A) ...",
    "explanation": "..."
  }}
]

Rules:
- Exactly 4 options
- Answer must match one option exactly
- No extra text outside JSON
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        raw_text = response.choices[0].message.content
        raw = extract_json(raw_text)
        questions = json.loads(raw)

        if not isinstance(questions, list):
            raise ValueError("Invalid format")

        return jsonify({"questions": questions})

    except json.JSONDecodeError:
        return jsonify({"error": "Model returned invalid JSON"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Serve frontend ───────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)