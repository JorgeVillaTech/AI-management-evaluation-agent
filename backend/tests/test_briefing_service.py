from unittest.mock import patch
from app.services.briefing_service import build_meeting_briefing


def test_briefing_with_only_internal_data():
    """A fictional company: has risk data, no real market data."""
    with patch("app.services.briefing_service.search_ticker", return_value=None):
        result = build_meeting_briefing("Acme Corp")

    assert result["market_data_available"] is False
    assert result["risk_level"] == "High"
    assert "error" not in result


def test_briefing_with_only_market_data():
    """A real company not in our seeded database: market data, no risk profile."""
    fake_market_data = {
        "ticker": "AAPL", "name": "Apple Inc", "exchange": "NASDAQ",
        "industry": "Technology", "market_cap": 4000000, "current_price": 326.57,
        "day_change_percent": 1.2,
    }
    with patch("app.services.briefing_service.search_ticker", return_value={"symbol": "AAPL", "description": "Apple Inc"}), \
        patch("app.services.briefing_service.get_market_data", return_value=fake_market_data):
        result = build_meeting_briefing("Apple")

    assert result["risk_level"] is None
    assert result["market_data_available"] is True
    assert result["current_price"] == 326.57


def test_briefing_fails_gracefully_when_both_sources_missing():
    with patch("app.services.briefing_service.search_ticker", return_value=None):
        result = build_meeting_briefing("Totally Unknown Inc")

    assert "error" in result