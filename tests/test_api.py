import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "VeriTrueAI2.0 Backend"


def test_analyze_text():
    """Test text analysis endpoint."""
    response = client.post(
        "/api/v1/analyze/",
        json={
            "content": "The earth is flat and has been proven by scientists.",
            "media_type": "text",
            "metadata": {}
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "id" in data
    assert "verdict" in data
    assert "confidence" in data
    assert "confidence_score" in data
    assert "summary" in data
    assert "evidence" in data
    assert "reasoning" in data
    assert "timestamp" in data
    assert "processing_time" in data


def test_analyze_url():
    """Test URL analysis endpoint."""
    response = client.post(
        "/api/v1/analyze/",
        json={
            "content": "https://example.com/fake-news-article",
            "media_type": "url",
            "metadata": {}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "verdict" in data


def test_search_sources():
    """Test source search endpoint."""
    response = client.get("/api/v1/search-sources/?query=covid vaccine&limit=5")
    assert response.status_code == 200
    data = response.json()
    
    assert "sources" in data
    assert "total_found" in data
    assert "search_time" in data
    assert len(data["sources"]) <= 5


def test_search_credible_sources():
    """Test credible source search."""
    response = client.get(
        "/api/v1/search-sources/credible?query=climate change&limit=3&min_credibility=0.8"
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify all sources meet credibility threshold
    for source in data["sources"]:
        assert source["credibility_score"] >= 0.8


def test_get_history():
    """Test analysis history endpoint."""
    response = client.get("/api/v1/history/?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_analytics_overview():
    """Test analytics overview endpoint."""
    response = client.get("/api/v1/analytics/overview?days=7")
    assert response.status_code == 200
    data = response.json()
    
    assert "total_analyses" in data
    assert "verdicts_breakdown" in data
    assert "confidence_breakdown" in data
    assert "media_type_breakdown" in data


def test_user_settings():
    """Test user settings endpoints."""
    user_id = "test_user_123"
    
    # Get settings (should create defaults)
    response = client.get(f"/api/v1/settings/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert "preferences" in data
    assert "notification_settings" in data


def test_batch_analysis():
    """Test batch analysis endpoint."""
    response = client.post(
        "/api/v1/analyze/batch",
        json=[
            {
                "content": "Breaking news: major discovery announced",
                "media_type": "text",
                "metadata": {}
            },
            {
                "content": "Scientists confirm earth is round",
                "media_type": "text", 
                "metadata": {}
            }
        ]
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    for result in data:
        assert "verdict" in result
        assert "confidence" in result


def test_invalid_media_type():
    """Test invalid media type handling."""
    response = client.post(
        "/api/v1/analyze/",
        json={
            "content": "Test content",
            "media_type": "invalid_type",
            "metadata": {}
        }
    )
    assert response.status_code == 422  # Validation error


def test_empty_content():
    """Test empty content handling."""
    response = client.post(
        "/api/v1/analyze/",
        json={
            "content": "",
            "media_type": "text",
            "metadata": {}
        }
    )
    # Should still process but may return low confidence
    assert response.status_code in [200, 400]


def test_large_batch():
    """Test batch size limit."""
    large_batch = [
        {
            "content": f"Test content {i}",
            "media_type": "text",
            "metadata": {}
        }
        for i in range(15)  # More than max batch size of 10
    ]
    
    response = client.post("/api/v1/analyze/batch", json=large_batch)
    assert response.status_code == 400  # Should reject large batch