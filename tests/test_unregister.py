"""Tests for the unregister endpoint"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_unregister_success():
    """Test successful unregistration from an activity"""
    email = "unregister_test@example.com"
    
    # Sign up first
    client.post("/activities/Science%20Club/signup?email=" + email)
    
    # Then unregister
    response = client.delete(
        f"/activities/Science%20Club/unregister?email={email}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Science Club" in data["message"]


def test_unregister_nonexistent_activity():
    """Test that unregistering from a non-existent activity fails"""
    response = client.delete(
        "/activities/Fake%20Club/unregister?email=test@example.com"
    )
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_unregister_not_registered():
    """Test that unregistering a non-registered email fails"""
    response = client.delete(
        "/activities/Basketball%20Team/unregister?email=not_registered@example.com"
    )
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"].lower()


def test_unregister_removes_participant():
    """Test that unregistering actually removes the participant from the activity"""
    email = "verify_removal@example.com"
    activity_name = "Debate%20Team"
    
    # Sign up
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Verify signup by checking activities
    response = client.get("/activities")
    assert email in response.json()["Debate Team"]["participants"]
    
    # Unregister
    client.delete(f"/activities/{activity_name}/unregister?email={email}")
    
    # Verify removal by checking activities again
    response = client.get("/activities")
    assert email not in response.json()["Debate Team"]["participants"]


def test_unregister_cannot_unregister_twice():
    """Test that unregistering the same person twice fails"""
    email = "double_unregister@example.com"
    activity_name = "Gym%20Class"
    
    # Sign up
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # First unregister succeeds
    response1 = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    assert response1.status_code == 200
    
    # Second unregister fails
    response2 = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "not registered" in data["detail"].lower()


def test_unregister_response_contains_message():
    """Test that successful unregister returns a message"""
    email = "message_check@example.com"
    
    # Sign up first
    client.post("/activities/Art%20Studio/signup?email=" + email)
    
    # Unregister
    response = client.delete(
        f"/activities/Art%20Studio/unregister?email={email}"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0
