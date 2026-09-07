from dotenv import load_dotenv
load_dotenv()

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

from app.agent.tools import get_company_profile, list_all_companies

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
    ),
    tools=[get_company_profile, list_all_companies],
)