from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


# Test 1: Home endpoint

def test_home():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["app"] == "LegalEase"

    assert data["status"] == "running"


# Test 2: Health endpoint

def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


# Test 3: Missing fields validation

def test_generate_invalid_request():

    response = client.post(
        "/generate",
        json={
            "document_type": "NDA"
        }
    )

    assert response.status_code == 422


# Test 4: Empty input validation

def test_generate_empty_request():

    response = client.post(
        "/generate",
        json={
            "document_type": "",
            "parties": "",
            "terms": "",
            "effective_date": ""
        }
    )

    assert response.status_code == 422


# Test 5: Invalid endpoint

def test_invalid_endpoint():

    response = client.get("/invalid")

    assert response.status_code == 404