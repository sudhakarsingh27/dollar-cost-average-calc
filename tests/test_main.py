import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from main import app

client = TestClient(app)

# Fixture for common test data
@pytest.fixture
def valid_investment_data():
    today = datetime.now()
    start_date = (today - timedelta(days=365)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    
    return {
        "ticker": "AAPL",
        "amount": 100,
        "frequency": "monthly",
        "start_date": start_date,
        "end_date": end_date
    }

def test_read_root():
    """Test the home page endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_calculator_page():
    """Test the calculator page endpoint"""
    response = client.get("/calculator")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_submit_dates_valid_data(valid_investment_data):
    """Test the submit_dates endpoint with valid data"""
    response = client.post("/api/submit-dates", json=valid_investment_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "symbol" in data
    assert "amount" in data
    assert "frequency" in data
    assert "results" in data
    
    # Check results structure
    results = data["results"]
    for frequency in ["daily", "weekly", "monthly"]:
        assert frequency in results
        assert "profit_loss" in results[frequency]
        assert "total_invested" in results[frequency]
        assert isinstance(results[frequency]["profit_loss"], (int, float))
        assert isinstance(results[frequency]["total_invested"], (int, float))

def test_submit_dates_invalid_ticker():
    """Test with invalid ticker symbol"""
    invalid_data = {
        "ticker": "INVALID_TICKER_123",
        "amount": 100,
        "frequency": "monthly",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }
    response = client.post("/api/submit-dates", json=invalid_data)
    assert response.status_code == 400

def test_submit_dates_invalid_frequency():
    """Test with invalid frequency"""
    invalid_data = {
        "ticker": "AAPL",
        "amount": 100,
        "frequency": "invalid_frequency",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }
    response = client.post("/api/submit-dates", json=invalid_data)
    assert response.status_code == 400

def test_submit_dates_invalid_dates():
    """Test with invalid date format"""
    invalid_data = {
        "ticker": "AAPL",
        "amount": 100,
        "frequency": "monthly",
        "start_date": "invalid-date",
        "end_date": "2023-12-31"
    }
    response = client.post("/api/submit-dates", json=invalid_data)
    assert response.status_code == 400

def test_submit_dates_future_dates():
    """Test with future dates"""
    future_data = {
        "ticker": "AAPL",
        "amount": 100,
        "frequency": "monthly",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31"
    }
    response = client.post("/api/submit-dates", json=future_data)
    assert response.status_code == 400

def test_submit_dates_negative_amount():
    """Test with negative investment amount"""
    invalid_data = {
        "ticker": "AAPL",
        "amount": -100,
        "frequency": "monthly",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }
    response = client.post("/api/submit-dates", json=invalid_data)
    assert response.status_code == 400

def test_submit_dates_missing_fields():
    """Test with missing required fields"""
    invalid_data = {
        "ticker": "AAPL",
        # missing amount
        "frequency": "monthly",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }
    response = client.post("/api/submit-dates", json=invalid_data)
    assert response.status_code == 400

def test_investment_calculations(valid_investment_data):
    """Test the actual investment calculations"""
    response = client.post("/api/submit-dates", json=valid_investment_data)
    assert response.status_code == 200
    
    data = response.json()
    results = data["results"]
    print(results)
    
    # Test that calculations make sense
    for frequency in ["daily", "weekly", "monthly"]:
        assert results[frequency]["total_invested"] > 0
        # Total invested should be approximately the same across frequencies
        assert abs(results[frequency]["total_invested"] - 
                  results["monthly"]["total_invested"]) / results["monthly"]["total_invested"] < 0.1

def test_static_files():
    """Test that static files are being served"""
    response = client.get("/static/js/calculator.js")
    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"] 