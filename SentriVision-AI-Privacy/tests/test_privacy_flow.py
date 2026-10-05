from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_end_to_end_privacy_flow():
    # 1. ORIGINAL WEBPAGE TEXT
    original_text = "My Account Number: 123456789012 and my email is afrin@example.com."
    
    # 2. LOCAL PRIVACY GATEWAY PROCESSES TEXT
    response_sanitize = client.post("/sanitize", json={"text": original_text})
    assert response_sanitize.status_code == 200
    sanitize_data = response_sanitize.json()
    
    sanitized_text = sanitize_data["sanitized_text"]
    
    # 3. VERIFY SANITIZATION
    assert "123456789012" not in sanitized_text
    assert "afrin@example.com" not in sanitized_text
    assert "[BANK ACCOUNT REDACTED]" in sanitized_text
    assert "[EMAIL REDACTED]" in sanitized_text
    
    # 4. SEND TO AI
    response_ai = client.post("/ai/process", json={"text": sanitized_text})
    assert response_ai.status_code == 200
    ai_data = response_ai.json()
    
    # 5. VERIFY AI RECEIVES SAFE PAYLOAD
    ai_received = ai_data["received_by_ai"]
    
    # This is the central privacy claim proof
    assert "123456789012" not in ai_received, "CRITICAL PRIVACY FAILURE: Account sent to AI"
    assert "afrin@example.com" not in ai_received, "CRITICAL PRIVACY FAILURE: Email sent to AI"
    assert "[BANK ACCOUNT REDACTED]" in ai_received
    assert "[EMAIL REDACTED]" in ai_received
    assert ai_data["privacy_safe"] == True
