"""Tests for the signup endpoint"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_signup_success():
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=test@example.com",
        headers={"content-type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "test@example.com" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_duplicate_email():
    """Test that signing up twice with the same email fails"""
    email = "duplicate@example.com"
    
    # First signup should succeed
    response1 = client.post(
        "/activities/Programming%20Class/signup?email=duplicate@example.com"
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        "/activities/Programming%20Class/signup?email=duplicate@example.com"
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity():
    """Test that signing up for a non-existent activity fails"""
    response = client.post(
        "/activities/Nonexistent%20Club/signup?email=test@example.com"
    )
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_multiple_participants():
    """Test that multiple different participants can sign up"""
    emails = ["participant1@example.com", "participant2@example.com", "participant3@example.com"]
    
    for email in emails:
        response = client.post(
            f"/activities/Tennis%20Club/signup?email={email}"
        )
        assert response.status_code == 200


def test_signup_email_format():
    """Test that signup accepts email in various formats"""
    response = client.post(
        "/activities/Drama%20Club/signup?email=student.name+tag@school.edu"
    )
    assert response.status_code == 200


def test_signup_response_contains_message():
    """Test that successful signup returns a message"""
    response = client.post(
        "/activities/Art%20Studio/signup?email=artist@example.com"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0
