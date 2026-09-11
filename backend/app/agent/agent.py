from dotenv import load_dotenv
load_dotenv()

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

from app.agent.tools import get_company_profile, list_all_companies,generate_formal_report, get_market_data_tool, prepare_meeting_briefing, get_portfolio_risk_summary, compare_to_peers

risk_advisor_agent = Agent(
    client=OpenAIChatClient(),
    name="RiskAdvisor",
    description="Advises company's relationship managers on company risk profiles and growth opportunities before client meetings.",
    instructions=(
        "You are an internal risk and growth advisory assistant for a company's"
        "relationship managers. You help them quickly understand a company's "
        "risk profile before client meetings. Always use the get_company_profile "
        "tool to retrieve real data before answering — never guess or invent "
        "financial information. If a company isn't found, say so clearly."
        "... You can generate a formal compliance report using generate_formal_report, you have the tool for this, use formal colors and format."
        "...You can also retrieve real, live market data (current price, market cap, exchange) "
        "using get_market_data_tool when the user asks about a company's actual market standing, "
        "separate from its internal risk score."

    ),
    tools=[get_company_profile, list_all_companies, generate_formal_report, get_market_data_tool, prepare_meeting_briefing, get_portfolio_risk_summary, compare_to_peers],
)