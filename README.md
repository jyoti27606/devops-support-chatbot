# DevOps Support Chatbot

An AI-assisted DevOps troubleshooting chatbot backend built with Python and FastAPI. It helps users identify common DevOps problems and provides possible causes, troubleshooting steps, extra tips, and official documentation links.

## Features

- Knowledge base containing 30 common DevOps issues.
- Keyword-based search to find relevant troubleshooting guidance.
- Structured answers: Problem, Likely Cause, Fix Steps, and Extra Tips.
- Follow-up questions when a problem is vague.
- Uncertainty handling when no strong match is found.
- Basic detection of messages that may contain secrets.
- Feedback endpoint supporting thumbs-up and thumbs-down ratings.
- 20 automated tests using pytest.

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- Pytest

## Project Structure

```text
devops-support-chatbot/
├── backend/
│   ├── main.py
│   ├── knowledge_base.json
│   ├── feedback.json
│   └── test_main.py
└── README.md
```

`feedback.json` is created automatically when feedback is submitted.

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/jyoti27606/devops-support-chatbot.git
cd devops-support-chatbot
```

Replace the placeholder with the actual repository URL.

### 2. Install dependencies

```bash
python -m pip install fastapi uvicorn pytest httpx
```

### 3. Start the backend

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open the API documentation

Visit:

```text
http://127.0.0.1:8000/docs
```

Available endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check the welcome message |
| GET | `/health` | Check backend health and knowledge-base count |
| POST | `/chat` | Submit a DevOps problem |
| POST | `/feedback` | Submit feedback on an answer |

## Example Chat Request

```json
{
  "message": "My Kubernetes pod is showing ImagePullBackOff"
}
```

The response includes a troubleshooting answer and, where relevant, related issues.

## Example Feedback Request

```json
{
  "issue_id": 5,
  "rating": "up",
  "comment": "The solution was helpful."
}
```

The rating must be `up` or `down`.

## Run Automated Tests

From the repository root, run:

```bash
python -m pytest backend/test_main.py -v
```

The current test suite contains 20 automated tests covering API endpoints, knowledge-base search, follow-up questions, unknown issues, secret detection, feedback validation, and answer structure.

## Safety Notes

- Do not submit passwords, API keys, access tokens, private keys, or confidential customer data.
- Secret detection uses basic patterns and cannot identify every possible secret.
- Troubleshooting steps are suggestions; review commands before executing them, especially in production environments.
- Apply least-privilege permissions when working with cloud resources.
- Verify recommendations against the linked official documentation.

## Current Limitations

- Search uses keyword matching rather than an AI language model or semantic search.
- Feedback is stored in a local JSON file, not a database.
- The secret detection is not exhaustive.
- Deployment and integration with the frontend must be configured separately.

## Future Improvements

- Expand and improve search relevance.
- Add a database for feedback storage.
- Support log-file uploads and error summaries.
- Add source citations and related-issue recommendations.
- Add deployment configuration and containerization.

## Project Status

Backend API, 30 knowledge-base entries, feedback storage, and a 20-test automated suite have been implemented. Further integration, testing, and deployment work may still be required.
