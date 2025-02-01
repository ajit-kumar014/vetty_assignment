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
    if api_key != API_KEY:
        raise HTTPException(401, "Invalid API Key")
    return api_key

def check_coingecko():
    try:
        response = requests.get(f"{COINGECKO_URL}/ping", timeout=5)
        if response.status_code == 200:
            return True, response.json().get("gecko_says", "")
        return False, ""
    except requests.exceptions.RequestException:
        return False, ""

@app.get("/health", tags=["Monitoring"])
async def health_check():
    coingecko_up, _ = check_coingecko()
    return {
        "service_status": "healthy",
        "third_party_services": {
            "coingecko": "operational" if coingecko_up else "unavailable"
        }
    }

@app.get("/version", tags=["Monitoring"])
async def version_info():
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

@app.get("/coins", tags=["Cryptocurrency"])
def list_coins(page_num: int = 1, per_page: int = 10, _: str = Depends(auth)):
    response = requests.get(f"{COINGECKO_URL}/coins/markets", params={"vs_currency": "cad", "page": page_num, "per_page": per_page})
    return response.json()

@app.get("/categories", tags=["Cryptocurrency"])
async def list_categories(_: str = Depends(auth)):
    return requests.get(f"{COINGECKO_URL}/coins/categories").json()
