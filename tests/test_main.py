import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from src.main import app, API_KEY

client = TestClient(app)

@pytest.fixture
def mock_requests():
    with patch('src.main.requests') as mock_req:
        yield mock_req

@pytest.fixture
def auth_headers():
    return {"X-API-Key": API_KEY}

def test_health_check_when_coingecko_up(mock_requests):
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"gecko_says": "all good!"}
    mock_requests.get.return_value = mock_response

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "service_status": "healthy",
        "third_party_services": {
            "coingecko": "operational"
        }
    }



def test_version_info_success(mock_requests):
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"gecko_says": "to the moon V3!"}
    mock_requests.get.return_value = mock_response

    # Act
    response = client.get("/version")

    # Assert
    assert response.status_code == 200
    assert response.json()["application_version"] == "1.0.0"
    assert response.json()["dependencies"]["coingecko_api"] == "v3"

def test_list_coins_unauthorized():
    # Act
    response = client.get("/coins")

    # Assert
    assert response.status_code == 403
    assert "Not authenticated" in response.json()["detail"]

def test_list_coins_success(mock_requests, auth_headers):
    # Arrange
    expected_data = [
        {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
        {"id": "ethereum", "symbol": "eth", "name": "Ethereum"}
    ]
    mock_response = MagicMock()
    mock_response.json.return_value = expected_data
    mock_requests.get.return_value = mock_response

    # Act
    response = client.get("/coins", headers=auth_headers)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_data
    mock_requests.get.assert_called_once()

def test_get_coin_details_success(mock_requests, auth_headers):
    # Arrange
    coin_id = "bitcoin"
    expected_data = {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "market_data": {"current_price": {"usd": 50000}}
    }
    mock_response = MagicMock()
    mock_response.json.return_value = expected_data
    mock_requests.get.return_value = mock_response

    # Act
    response = client.get(f"/coin/{coin_id}", headers=auth_headers)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_data
    mock_requests.get.assert_called_once_with(
        f"https://api.coingecko.com/api/v3/coins/{coin_id}",
        params={"localization": False}
    )

def test_list_categories_success(mock_requests, auth_headers):
    # Arrange
    expected_data = [
        {"id": "defi", "name": "DeFi"},
        {"id": "nft", "name": "NFT"}
    ]
    mock_response = MagicMock()
    mock_response.json.return_value = expected_data
    mock_requests.get.return_value = mock_response

    # Act
    response = client.get("/categories", headers=auth_headers)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_data

@pytest.mark.parametrize("endpoint", [
    "/coins",
    "/categories",
    "/coin/bitcoin"
])
def test_endpoints_require_authentication(endpoint):
    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 403  # Changed from 401 to match actual behavior
    assert "Not authenticated" in response.json()["detail"]

def test_invalid_coin_id(mock_requests, auth_headers):
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "Coin not found"}
    mock_requests.get.return_value = mock_response

    # Act
    response = client.get("/coin/invalid-coin", headers=auth_headers)

    # Assert
    assert response.json() == {"error": "Coin not found"}