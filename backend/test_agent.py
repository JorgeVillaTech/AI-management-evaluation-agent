import asyncio
from app.agent.agent import risk_advisor_agent


async def main():
    result = await risk_advisor_agent.run("What's the risk profile for Acme Corp?")
    print(result.text)

    result2 = await risk_advisor_agent.run("What about a company called Nonexistent Inc?")
    print(result2.text)

    result3 = await risk_advisor_agent.run("Which are the companies you have registered?")
    print(result3.text)

    result4 = await risk_advisor_agent.run("What's the current market data for Apple?")
    print(result4.text)

    result5 = await risk_advisor_agent.run("Prepare a meeting briefing for Acme Corp.")
    print(result5.text)

    result6 = await risk_advisor_agent.run("Which companies in my portfolio need attention right now?")
    print(result6.text)


if __name__ == "__main__":
    asyncio.run(main())