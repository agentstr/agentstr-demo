from dotenv import load_dotenv
from pynostr.key import PrivateKey

load_dotenv()

import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agentstr import AgentCard, ChatInput, NostrAgentServer, Skill

# Get the environment variables
relays = os.getenv('NOSTR_RELAYS').split(',')
private_key = os.getenv('AGENT_PRIVATE_KEY')
nwc_str = os.getenv('AGENT_NWC_CONN_STR')

# Define model
model = OpenAIChat(
    temperature=0,
    base_url=os.getenv('LLM_BASE_URL'),
    api_key=os.getenv('LLM_API_KEY'),
    id=os.getenv('LLM_MODEL_NAME')
)

# Define Agno agent
agent = Agent(
    model=model,
    tools=[
        ReasoningTools(add_instructions=True, analyze=True, think=True),
        YFinanceTools(stock_price=True, historical_prices=True) #, analyst_recommendations=True, company_info=True, company_news=True),
    ],
    instructions=[
        "Use tables to display data",
        "Only output the report, no other text",
    ],
    markdown=True,
)

# Define agent callable
async def agent_callable(input: ChatInput) -> str:    
    result = await agent.arun(message=input.messages[-1], session_id=input.thread_id)
    return result.content

# Create Nostr Agent Server
async def run():
    agent_info = AgentCard(
    name='Finance Agent',
    description=('This agent can help you find historical price data for stocks.'),
    skills=[
        Skill(name='stock_price', description='Get the current price of a stock.', satoshis=0),
        Skill(name='historical_prices', description='Get the historical prices of a stock.', satoshis=0),
    ],
    satoshis=10,
    nostr_pubkey=PrivateKey.from_nsec(private_key).public_key.bech32(),
)
    server = NostrAgentServer(relays=relays,
                              private_key=private_key,
                              agent_callable=agent_callable,
                              agent_info=agent_info,
                              nwc_str=nwc_str,
                              router_llm=lambda message: model.ainvoke(message).content)
    await server.start()


if __name__ == '__main__':
    import asyncio
    asyncio.run(run())