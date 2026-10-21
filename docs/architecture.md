# DevOps Support Chatbot — Architecture

```mermaid
flowchart TD
    A[User / Chat Interface] --> B[FastAPI Backend]
    B --> C[Input Validation and Safety Checks]
    C --> D[Knowledge Base Search]
    D --> E[knowledge_base.json - 30 Issues]
    E --> F[Structured Troubleshooting Answer]
    B --> G[Feedback Endpoint]
    G --> H[feedback.json]
    I[Automated Tests - 20] --> B
```

## Components

- **FastAPI Backend:** Handles chat and feedback requests.
- **Knowledge Base:** Contains 30 common DevOps issues, their likely causes, fixes, tips, and sources.
- **Search:** Matches user queries with relevant knowledge-base issues.
- **Feedback:** Stores helpful or unhelpful ratings.
- **Automated Tests:** Checks API endpoints and expected chatbot behavior.

## Response Format

Problem → Likely Cause → Fix Steps → Extra Tips
