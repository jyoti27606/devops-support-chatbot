# DevOps Support Chatbot — Test Report

## 1. Test Summary

- **Project:** Team A DevOps Support Chatbot
- **Framework:** Pytest, FastAPI TestClient
- **Total test cases:** 20
- **Passed:** 20
- **Failed:** 0
- **Result:** All 20 automated tests passed
- **Warning:** One non-blocking deprecation warning

## 2. Test Cases and Results

| No. | Test case | Expected result | Status |
|---:|---|---|---|
| 1 | Home endpoint | Returns a valid response | PASS |
| 2 | Health endpoint | Reports healthy status and 30 issues | PASS |
| 3 | Kubernetes ImagePullBackOff | Returns relevant troubleshooting steps | PASS |
| 4 | AWS S3 AccessDenied | Returns relevant troubleshooting guidance | PASS |
| 5 | Vague problem description | Requests more information | PASS |
| 6 | Unknown issue | Responds without inventing a solution | PASS |
| 7 | Secret-like input | Triggers a security warning | PASS |
| 8 | Submit feedback | Saves feedback successfully | PASS |
| 9 | HTTP 503 error | Returns relevant troubleshooting guidance | PASS |
| 10 | Git merge conflict | Returns relevant troubleshooting guidance | PASS |
| 11 | Docker port conflict | Returns relevant troubleshooting guidance | PASS |
| 12 | Kubernetes Pending | Returns relevant troubleshooting guidance | PASS |
| 13 | HTTP 504 error | Returns relevant troubleshooting guidance | PASS |
| 14 | TLS certificate error | Returns relevant troubleshooting guidance | PASS |
| 15 | Empty chat message | Handles invalid input | PASS |
| 16 | Missing chat message | Validates the request | PASS |
| 17 | Invalid feedback rating | Rejects invalid rating | PASS |
| 18 | Missing feedback issue ID | Validates the request | PASS |
| 19 | Feedback comment over 500 characters | Rejects oversized comment | PASS |
| 20 | Chat answer structure | Checks required answer fields | PASS |

## 3. Test Execution

Command used:

```bash
python -m pytest backend/test_main.py -v
```

Final result:

```text
20 passed, 1 warning in 4.01s
```

## 4. Conclusion

All 20 automated tests passed. The tests cover API endpoints, DevOps troubleshooting, input validation, feedback handling, and response structure.

These results confirm the tested backend behaviors. They do not independently verify frontend integration, deployment, or every possible real-world DevOps scenario.

