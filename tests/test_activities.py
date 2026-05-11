"""Tests for the activities endpoint"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_list():
    """Test that GET /activities returns a list of all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_has_correct_structure():
    """Test that activity objects have the expected structure"""
    response = client.get("/activities")
    data = response.json()
    
    # Check that an activity has required fields
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity


def test_get_activities_participants_is_list():
    """Test that participants field contains a list"""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Chess Club"]
    assert isinstance(activity["participants"], list)


def test_get_activities_has_multiple_activities():
    """Test that the activities list contains multiple activities"""
    response = client.get("/activities")
    data = response.json()
    
    # Should have at least a few activities
    assert len(data) >= 5
