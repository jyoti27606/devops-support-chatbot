
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200


def test_health_reports_30_issues():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["knowledge_base_issues"] == 30


def test_chat_finds_image_pull_backoff():
    response = client.post(
        "/chat",
        json={"message": "Kubernetes ImagePullBackOff"}
    )
    assert response.status_code == 200
    assert "image" in response.json()["reply"]["problem"].lower()
    assert "source" in response.json()["reply"]


def test_chat_finds_s3_access_denied():
    response = client.post(
        "/chat",
        json={"message": "AWS S3 AccessDenied"}
    )
    assert response.status_code == 200
    assert "AccessDenied" in response.json()["reply"]["problem"]


def test_chat_asks_for_more_details():
    response = client.post(
        "/chat",
        json={"message": "My pod is failing"}
    )
    assert response.status_code == 200
    assert "follow_up_question" in response.json()


def test_chat_handles_unknown_issue():
    response = client.post(
        "/chat",
        json={"message": "My cloud deployment has a strange problem"}
    )
    assert response.status_code == 200
    assert "follow_up_question" in response.json()
    assert response.json()["matches"] == []


def test_chat_warns_about_possible_secret():
    response = client.post(
        "/chat",
        json={"message": "password=mysecret123"}
    )
    assert response.status_code == 200
    assert "Warning" in response.json()["reply"]


def test_feedback_is_saved():
    response = client.post(
        "/feedback",
        json={
            "issue_id": 5,
            "rating": "up",
            "comment": "Helpful answer"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"



def test_chat_finds_http_503():
    response = client.post(
        "/chat",
        json={"message": "My website returns HTTP 503 Service Unavailable"}
    )
    assert response.status_code == 200
    assert "503" in response.json()["reply"]["problem"]


def test_chat_finds_git_merge_conflict():
    response = client.post(
        "/chat",
        json={"message": "Git merge conflict in my deployment branch"}
    )
    assert response.status_code == 200
    assert "merge" in response.json()["reply"]["problem"].lower()


def test_chat_finds_docker_port_conflict():
    response = client.post(
        "/chat",
        json={"message": "Docker port conflict address already in use"}
    )
    assert response.status_code == 200
    assert "port" in response.json()["reply"]["problem"].lower()


def test_chat_finds_kubernetes_pending():
    response = client.post(
        "/chat",
        json={"message": "My Kubernetes pod is stuck Pending"}
    )
    assert response.status_code == 200
    assert "Pending" in response.json()["reply"]["problem"]


def test_chat_finds_http_504():
    response = client.post(
        "/chat",
        json={"message": "I am getting HTTP 504 Gateway Timeout"}
    )
    assert response.status_code == 200
    assert "504" in response.json()["reply"]["problem"]


def test_chat_finds_tls_error():
    response = client.post(
        "/chat",
        json={"message": "My application has an SSL certificate verify failed error"}
    )
    assert response.status_code == 200
    assert "TLS" in response.json()["reply"]["problem"] or \
           "certificate" in response.json()["reply"]["problem"].lower()


def test_chat_handles_empty_message():
    response = client.post(
        "/chat",
        json={"message": "   "}
    )
    assert response.status_code == 200
    assert "follow_up_question" in response.json()


def test_chat_rejects_missing_message():
    response = client.post("/chat", json={})
    assert response.status_code == 422


def test_feedback_rejects_invalid_rating():
    response = client.post(
        "/feedback",
        json={"issue_id": 5, "rating": "maybe", "comment": ""}
    )
    assert response.status_code == 422


def test_feedback_rejects_missing_issue_id():
    response = client.post(
        "/feedback",
        json={"rating": "up", "comment": "Helpful"}
    )
    assert response.status_code == 422


def test_feedback_rejects_long_comment():
    response = client.post(
        "/feedback",
        json={
            "issue_id": 5,
            "rating": "up",
            "comment": "x" * 501
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "error"


def test_chat_response_has_answer_sections():
    response = client.post(
        "/chat",
        json={"message": "Kubernetes ImagePullBackOff"}
    )
    body = response.json()["reply"]
    assert all(
        key in body
        for key in ["problem", "likely_cause", "fix_steps", "extra_tips", "source"]
    )
