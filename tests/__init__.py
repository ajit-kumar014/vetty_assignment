"""
Test suite for the Cryptocurrency API Service.

Contains unit tests, integration tests, and fixtures for testing
the API endpoints and service functionality.
"""

import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define test constants
TEST_API_KEY = "test_api_key"
MOCK_COIN_DATA = {
    "bitcoin": {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin"
    },
    "ethereum": {
        "id": "ethereum",
        "symbol": "eth",
        "name": "Ethereum"
    }
}

@pytest.fixture
def mock_coin_data():
    return MOCK_COIN_DATA.copy()
