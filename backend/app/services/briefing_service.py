from app.services.company_service import find_company
from app.services.market_data_service import search_ticker, get_market_data


def build_meeting_briefing(company_name: str) -> dict:
    risk_profile = find_company(company_name)
    ticker_match = search_ticker(company_name)
    market_data = get_market_data(ticker_match["symbol"]) if ticker_match else None

    if risk_profile is None and market_data is None:
        return {"error": f"No internal risk profile or market data found for '{company_name}'"}

    risk_level = None
    talking_points = []

    if risk_profile:
        risk_score = risk_profile["risk_score"]
        risk_level = "High" if risk_score >= 60 else "Moderate" if risk_score >= 35 else "Low"
        talking_points.append(f"Risk level is {risk_level.lower()} ({risk_score}/100), trending {risk_profile['trend']}.")
        talking_points.extend(f"Recent development: {s}" for s in risk_profile["recent_signals"])
    else:
        talking_points.append("No internal risk profile on file for this company yet.")

    if market_data:
        talking_points.append(
            f"Currently trading at ${market_data['current_price']} on {market_data['exchange']} "
            f"({market_data['day_change_percent']:+.2f}% today)."
        )

    return {
        "company_name": risk_profile["name"] if risk_profile else (ticker_match["description"] if ticker_match else company_name),
        "risk_score": risk_profile["risk_score"] if risk_profile else None,
        "risk_level": risk_level,
        "sector": risk_profile["sector"] if risk_profile else (market_data["industry"] if market_data else None),
        "market_data_available": market_data is not None,
        "current_price": market_data["current_price"] if market_data else None,
        "exchange": market_data["exchange"] if market_data else None,
        "talking_points": talking_points,
    }