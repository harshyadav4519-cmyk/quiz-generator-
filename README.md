# QuizAI – AI Quiz Generator

An AI-powered MCQ quiz generator built with **Python + Flask + Google Gemini API** and a clean **HTML/CSS/JS** frontend.

## Features
- Generate quizzes on any **topic** or paste your **syllabus/notes**
- Choose **difficulty**: Easy / Medium / Hard
- Set **number of questions** (3–20)
- Optional **countdown timer** per question
- **Instant feedback** with explanations after each answer
- **Score screen** with grade, stats, and full answer review

## Tech Stack
`Python` · `Flask` · `Google Gemini API` · `Prompt Engineering` · `JSON Parsing` · `HTML/CSS/JS`

---

## Setup & Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a Gemini API Key
- Go to https://aistudio.google.com/app/apikey
- Create a free API key

### 3. Set your API key

**Option A – Environment variable (recommended)**
```bash
# macOS/Linux
export GEMINI_API_KEY="your_key_here"

# Windows CMD
set GEMINI_API_KEY=your_key_here

# Windows PowerShell
$env:GEMINI_API_KEY="your_key_here"
```

**Option B – Edit app.py directly**
```python
GEMINI_API_KEY = "your_key_here"
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

---

## Project Structure
```
ai-quiz-generator/
├── app.py           # Flask backend + Gemini API logic
├── index.html       # Frontend (HTML/CSS/JS)
├── requirements.txt
└── README.md
```

---

## How It Works
1. User inputs a topic or syllabus, selects difficulty and number of questions
2. Flask backend crafts a structured prompt and calls the Gemini API
3. Gemini returns a JSON array of MCQ questions
4. Frontend dynamically renders the quiz with timer, scoring, and feedback
