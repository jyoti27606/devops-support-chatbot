
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from pathlib import Path
import json
import re

app = FastAPI(title="DevOps Support Chatbot", version="0.2.0")

KNOWLEDGE_FILE = Path(__file__).parent / "knowledge_base.json"


class ChatRequest(BaseModel):
    message: str


class FeedbackRequest(BaseModel):
    issue_id: int
    rating: Literal["up", "down"]
    comment: str = ""


def load_knowledge():
    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []



def search_knowledge(message):
    issues = load_knowledge()
    query = message.lower()
    query_words = set(re.findall(r"[a-z0-9]+", query))

    stop_words = {
        "a", "an", "the", "is", "are", "was", "were",
        "in", "on", "at", "to", "for", "of", "and",
        "my", "me", "i", "it", "what", "how", "why",
        "please", "help", "with", "when", "do", "does"
    }
    query_words -= stop_words

    matches = []

    for issue in issues:
        title = issue.get("title", "").lower()
        keywords = [
            keyword.lower()
            for keyword in issue.get("keywords", [])
        ]

        score = 0

        # Exact keyword phrases get the highest score.
        for keyword in keywords:
            if keyword in query:
                score += 10 + len(keyword.split())

        # Exact issue title is also a strong match.
        if title in query or query in title:
            score += 12

        # Give partial matches less importance.
        title_words = set(re.findall(r"[a-z0-9]+", title))
        score += 2 * len(query_words & title_words)

        keyword_words = set()
        for keyword in keywords:
            keyword_words.update(
                re.findall(r"[a-z0-9]+", keyword)
            )

        score += 3 * len(query_words & keyword_words)

        if score > 0:
            matches.append((score, issue))

    matches.sort(key=lambda item: item[0], reverse=True)

    # Return only strong matches.
    if not matches or matches[0][0] < 8:
        return []

    best_score = matches[0][0]

    return [
        issue
        for score, issue in matches
        if score >= max(5, best_score * 0.4)
    ][:3]


def format_answer(issue):
    return {
        "problem": issue["problem"],
        "likely_cause": issue["likely_cause"],
        "fix_steps": issue["fix_steps"],
        "extra_tips": issue["extra_tips"],
        "source": issue["source"]
    }


@app.get("/")
def home():
    return {"message": "DevOps Support Chatbot Backend is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "knowledge_base_issues": len(load_knowledge())}


@app.post("/chat")

def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        return {
            "reply": "Please describe your DevOps problem or paste the error message.",
            "follow_up_question": "Which tool are you using, and what error are you seeing?"
        }

    # Warn users if their message appears to contain a secret.
    secret_patterns = [
        r"AKIA[0-9A-Z]{16}",
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"(?i)\b(password|passwd|secret_access_key|api_key|access_token)\s*[:=]\s*\S+",
        r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"
    ]

    if any(re.search(pattern, message) for pattern in secret_patterns):
        return {
            "reply": (
                "Warning: Your message may contain a password, API key, "
                "token, or other secret. Do not share sensitive information. "
                "Remove it and send the error again."
            ),
            "matches": []
        }

    # Ask for more details when the problem is too vague.
    vague_phrases = [
        "not working",
        "something went wrong",
        "having a problem",
        "having an issue",
        "it is failing",
        "its failing",
        "my pod is failing",
        "help me"
    ]

    if len(message.split()) <= 5 and any(
        phrase in message.lower() for phrase in vague_phrases
    ):
        return {
            "reply": "I need a little more information to identify the problem.",
            "follow_up_question": (
                "Which tool are you using, what were you trying to do, "
                "and what exact error message did you get?"
            ),
            "matches": []
        }

    matches = search_knowledge(message)

    if not matches:
        return {
            "reply": (
                "I'm not sure about this issue yet. Please share the exact "
                "error message, the tool involved, and what you were trying "
                "to do. You can also consult the official documentation."
            ),
            "follow_up_question": (
                "Which DevOps tool are you using, and what error appears?"
            ),
            "matches": []
        }

    return {
        "reply": format_answer(matches[0]),
        "related_issues": [
            {
                "id": issue["id"],
                "title": issue["title"]
            }
            for issue in matches[1:]
        ]
    }



FEEDBACK_FILE = Path(__file__).parent / "feedback.json"


@app.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    if len(request.comment) > 500:
        return {
            "status": "error",
            "message": "Feedback comment must be 500 characters or less."
        }

    feedback_entries = []

    if FEEDBACK_FILE.exists():
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
                feedback_entries = json.load(file)
            if not isinstance(feedback_entries, list):
                feedback_entries = []
        except (json.JSONDecodeError, OSError):
            feedback_entries = []

    entry = {
        "issue_id": request.issue_id,
        "rating": request.rating,
        "comment": request.comment.strip()
    }

    feedback_entries.append(entry)

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as file:
        json.dump(feedback_entries, file, indent=2)

    return {
        "status": "success",
        "message": "Feedback saved successfully."
    }
