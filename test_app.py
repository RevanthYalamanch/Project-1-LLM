import pytest as pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# Test cases that are expected to pass with a 200 OK status
passing_test_cases = [
    ("PASS-01: Basic Valid Input", "Hello, how are you?"),
    ("PASS-02: Input with Numbers & Punctuation", "What is the value of pi (3.14)?"),
    ("PASS-03: Input with Whitespace", "  Tell me a joke.  "),
    ("PASS-04: Non-English Input", "¿Cómo estás?")
]

@pytest.mark.parametrize("name, message", passing_test_cases)
def test_chat_endpoint_passing_cases(name, message):
    """
    Tests the /chat endpoint with various valid inputs.
    """
    response = client.post("/chat", json={"message": message})
    assert response.status_code == 200
    json_response = response.json()
    assert "reply" in json_response
    assert isinstance(json_response["reply"], str)
    assert len(json_response["reply"]) > 0

# Test cases that are expected to fail with a 400 Bad Request status
failing_test_cases = [
    ("FAIL-01: Empty Message", "", "Message cannot be empty"),
    ("FAIL-02: Whitespace-Only Message", "   ", "Message cannot be empty"),
    ("FAIL-03: Message with Invalid Characters", "Is <b>this</b> valid?", "Invalid characters in message"),
    ("FAIL-04: Message Exceeds Max Length", "a" * 1001, "Message is too long")
]

@pytest.mark.parametrize("name, message, detail", failing_test_cases)
def test_chat_endpoint_failing_cases(name, message, detail):
    """
    Tests the /chat endpoint with various invalid inputs.
    """
    response = client.post("/chat", json={"message": message})
    assert response.status_code == 400
    assert response.json() == {"detail": detail}