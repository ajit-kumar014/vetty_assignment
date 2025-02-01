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
