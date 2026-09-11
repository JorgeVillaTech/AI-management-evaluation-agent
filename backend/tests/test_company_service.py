from app.services.company_service import find_company, list_companies


def test_find_company_returns_correct_data():
    result = find_company("Acme Corp")
    assert result is not None
    assert result["name"] == "Acme Corp"
    assert result["risk_score"] == 72


def test_find_company_is_case_insensitive():
    result = find_company("acme corp")
    assert result is not None
    assert result["name"] == "Acme Corp"


def test_find_company_returns_none_for_unknown_company():
    result = find_company("Definitely Not A Real Company XYZ")
    assert result is None


def test_list_companies_returns_all_seeded_companies():
    companies = list_companies()
    assert len(companies) == 30