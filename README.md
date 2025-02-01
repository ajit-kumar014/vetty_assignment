# Cryptocurrency API Service

A FastAPI-based REST API service that provides cryptocurrency market data by wrapping the CoinGecko API. This service includes authentication, health monitoring, and cryptocurrency data endpoints.

## Features

- Authentication via API key
- Health monitoring endpoints
- Version information tracking
- Cryptocurrency market data retrieval
- Rate limiting and pagination support
- Third-party service (CoinGecko) status monitoring

## Prerequisites

- Python 3.8+
- FastAPI
- Requests library
- A CoinGecko API account (free tier available)

## Local Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
export API_KEY=your_secret_key_here
```

## Docker Installation

Make sure docker is installed in the system.

```bash
docker compose up -d
```

Open the app at http://localhost:8001

## Configuration

The service can be configured using the following environment variables:

- `API_KEY`: Authentication key for accessing the API (default: "verystrongpassword")
- `COINGECKO_URL`: Base URL for CoinGecko API (default: "https://api.coingecko.com/api/v3")

## Running the Service

Start the service using uvicorn:

```bash
uvicorn src.main:app --reload
```

The service will be available at `http://localhost:8000`

## API Endpoints

### Swagger Endpoint

```
GET /docs
```

Returns the swagger API documentation.

### Monitoring

#### Health Check

```
GET /health
```

Returns the health status of the service and its dependencies.

#### Version Information

```
GET /version
```

Returns the application version and dependency versions.

### Cryptocurrency Data

#### List Coins

```
GET /coins
```

Parameters:

- `page_num` (optional): Page number for pagination (default: 1)
- `per_page` (optional): Number of items per page (default: 10)

Headers:

- `X-API-Key`: Required authentication key

#### List Categories

```
GET /categories
```

Returns available cryptocurrency categories.

Headers:

- `X-API-Key`: Required authentication key

#### Get Coin Details

```
GET /coin/{coin_id}
```

Parameters:

- `coin_id`: Identifier of the cryptocurrency

Headers:

- `X-API-Key`: Required authentication key

## Authentication

All cryptocurrency data endpoints require authentication using an API key. Include the key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your_api_key" http://localhost:8000/coins
```

## Error Handling

The service returns standard HTTP status codes:

- 200: Successful request
- 401: Invalid or missing API key
- 404: Resource not found
- 500: Internal server error

## Dependencies

- FastAPI: Web framework for building APIs
- Requests: HTTP library for making API calls
- Python-dotenv (recommended): Environment variable management

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 guidelines.
