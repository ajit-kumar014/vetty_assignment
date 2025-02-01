# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import APIKeyHeader
import requests
import os
import re

app = FastAPI()

API_KEY = os.getenv("API_KEY", "verystrongpassword")
COINGECKO_URL = "https://api.coingecko.com/api/v3"
APP_VERSION = "1.0.0"

api_key_header = APIKeyHeader(name="X-API-Key")

async def auth(api_key: str = Depends(api_key_header)):
    """
    Authenticate the provided API key.

    Args:
        api_key (str): The API key provided in the request header.

    Returns:
        str: The validated API key.

    Raises:
        HTTPException: If the provided API key is invalid.
    """
    if api_key != API_KEY:
        raise HTTPException(401, "Invalid API Key")
    return api_key

def check_coingecko():
    """
    Checks the status of the CoinGecko API.

    Sends a GET request to the CoinGecko API's ping endpoint to verify if the service is up and running.

    Returns:
        tuple: A tuple containing a boolean indicating the status of the API and a string message from the API.
               If the API is reachable and returns a status code of 200, the boolean is True and the message is
               the value of the "gecko_says" key from the JSON response. Otherwise, the boolean is False and
               the message is an empty string.
    """
    try:
        response = requests.get(f"{COINGECKO_URL}/ping", timeout=5)
        if response.status_code == 200:
            return True, response.json().get("gecko_says", "")
        return False, ""
    except requests.exceptions.RequestException:
        return False, ""


@app.get("/", tags=["Homepage"])
async def homepage():
    """
    Returns a description of the home page about the project and 
    directs the user to the Swagger documentation at the /docs endpoint.
    """
    return {
        "message": "Welcome to the project! Please visit the /docs endpoint for the Swagger documentation."
    }
    


@app.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Performs a health check for the service and its third-party dependencies.

    This asynchronous function checks the status of the Coingecko service and 
    returns a dictionary indicating the overall health status of the service 
    and the operational status of Coingecko.

    Returns:
        dict: A dictionary containing the health status of the service and 
        the operational status of third-party services.
        Example:
        {
    """
    coingecko_up, _ = check_coingecko()
    return {
        "service_status": "healthy",
        "third_party_services": {
            "coingecko": "operational" if coingecko_up else "unavailable"
        }
    }

@app.get("/version", tags=["Monitoring"])
async def version_info():
    """
    Fetches version information for the application and its dependencies.
    This asynchronous function checks the status of the CoinGecko API and extracts
    the version information from the response. If the API is reachable and the version
    information is found, it returns the version; otherwise, it defaults to "unknown".
    Returns:
        dict: A dictionary containing the application version and the CoinGecko API version.
        Example:
        {
            "application_version": "1.0.0",
                "coingecko_api": "v1"
    """
    coingecko_up, gecko_response = check_coingecko()
    version = "unknown"
    if coingecko_up:
        match = re.search(r"V(\d+)", gecko_response)
        version = f"v{match.group(1)}" if match else "unknown"
    
    return {
        "application_version": APP_VERSION,
        "dependencies": {
            "coingecko_api": version
        }
    }

@app.get("/coins", tags=["Cryptocurrency"], dependencies=[Depends(auth)])
def list_coins(page_num: int = 1, per_page: int = 10):
    """
    Fetches a list of cryptocurrency markets from the CoinGecko API.

    Args:
        page_num (int, optional): The page number to retrieve. Defaults to 1.
        per_page (int, optional): The number of items per page. Defaults to 10.

    Returns:
        list: A list of dictionaries containing market data for cryptocurrencies.
    """
    response = requests.get(f"{COINGECKO_URL}/coins/markets", params={"vs_currency": "cad", "page": page_num, "per_page": per_page})
    return response.json()

@app.get("/categories", tags=["Cryptocurrency"], dependencies=[Depends(auth)])
async def list_categories():
    """
    Fetches the list of cryptocurrency categories from the CoinGecko API.

    Returns:
        list: A list of dictionaries, each representing a cryptocurrency category.
    """
    return requests.get(f"{COINGECKO_URL}/coins/categories").json()

@app.get("/coin/{coin_id}", tags=["Cryptocurrency"], dependencies=[Depends(auth)])
def get_coin(coin_id: str):
    """
    Fetches the details of a cryptocurrency from the CoinGecko API.

    Args:
        coin_id (str): The unique identifier of the cryptocurrency.

    Returns:
        dict: A dictionary containing the details of the cryptocurrency.
    """
    response = requests.get(f"{COINGECKO_URL}/coins/{coin_id}", params={"localization": False})
    return response.json()