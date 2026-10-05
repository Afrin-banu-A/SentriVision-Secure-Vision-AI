from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["project"] == "SentriVision"
    assert data["mode"] == "local_privacy_gateway"

def test_detect_sensitive_text_normal():
    response = client.post("/detect-sensitive-text", json={"text": "Machine learning is useful for data analysis."})
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "NORMAL"
    assert data["detected"] == False
    assert len(data["entities"]) == 0

def test_detect_sensitive_text_supported_entity():
    # Using an explicitly supported pattern that matches the regex
    response = client.post("/detect-sensitive-text", json={"text": "Account Number: 123456789012"})
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "SENSITIVE"
    assert data["detected"] == True
    assert len(data["entities"]) > 0
    assert data["entities"][0]["placeholder"] == "[BANK ACCOUNT REDACTED]"
    assert data["protected_count"] > 0
    assert "123456789012" not in data["sanitized_text"]

def test_sanitize_text_mixed_content():
    # Normal content preserved, sensitive content redacted
    test_text = "Hello user. Your Account Number: 123456789012 is available."
    response = client.post("/sanitize", json={"text": test_text})
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "SENSITIVE"
    assert data["detected"] == True
    # The actual redaction replaces group 1 (the number itself), not the label.
    assert data["sanitized_text"] == "Hello user. Your Account Number: [BANK ACCOUNT REDACTED] is available."
    assert "123456789012" not in data["sanitized_text"]

def test_ai_process_unsafe_email():
    response = client.post("/ai/process", json={"text": "My email is test@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "REJECTED"
    assert data["privacy_safe"] == False

def test_ai_process_unsafe_account():
    response = client.post("/ai/process", json={"text": "Hello user. Your Account Number: 123456789012 is available."})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "REJECTED"
    assert data["privacy_safe"] == False

def test_ai_process_safe_account():
    response = client.post("/ai/process", json={"text": "Hello user. Your Account Number: [BANK ACCOUNT REDACTED] is available."})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ACCEPTED"
    assert data["privacy_safe"] == True
    assert data["received_by_ai"] == "Hello user. Your Account Number: [BANK ACCOUNT REDACTED] is available."

def test_ai_process_safe_normal():
    response = client.post("/ai/process", json={"text": "Machine learning is useful for data analysis."})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ACCEPTED"
    assert data["privacy_safe"] == True
    assert data["received_by_ai"] == "Machine learning is useful for data analysis."
