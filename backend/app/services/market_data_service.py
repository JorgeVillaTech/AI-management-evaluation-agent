import os
import requests

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"


def search_ticker(company_name: str) -> dict | None:
    """Resolves a company name to its stock ticker symbol using Finnhub's search endpoint."""
    api_key = os.getenv("FINNHUB_API_KEY")
    response = requests.get(
        f"{FINNHUB_BASE_URL}/search",
        params={"q": company_name, "token": api_key},
    )
    response.raise_for_status()
    results = response.json().get("result", [])

    if not results:
        return None

    best_match = results[0]
    return {"symbol": best_match["symbol"], "description": best_match["description"]}


def get_market_data(ticker: str) -> dict | None:
    """Fetches current market data (price, market cap, sector) for a given ticker from Finnhub."""
    api_key = os.getenv("FINNHUB_API_KEY")

    profile = requests.get(
        f"{FINNHUB_BASE_URL}/stock/profile2",
        params={"symbol": ticker, "token": api_key},
    ).json()

    quote = requests.get(
        f"{FINNHUB_BASE_URL}/quote",
        params={"symbol": ticker, "token": api_key},
    ).json()

    if not profile:
        return None

    return {
        "ticker": ticker,
        "name": profile.get("name"),
        "exchange": profile.get("exchange"),
        "industry": profile.get("finnhubIndustry"),
        "market_cap": profile.get("marketCapitalization"),
        "current_price": quote.get("c"),
        "day_change_percent": quote.get("dp"),
    }


def get_peers(ticker: str) -> list[str]:
    """Returns a list of peer company tickers in the same industry, from Finnhub."""
    api_key = os.getenv("FINNHUB_API_KEY")
    response = requests.get(
        f"{FINNHUB_BASE_URL}/stock/peers",
        params={"symbol": ticker, "token": api_key},
    )
    response.raise_for_status()
    return response.json()