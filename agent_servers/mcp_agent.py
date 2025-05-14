import os
from fastapi import FastAPI
from pynostr.key import PrivateKey
from pydantic import BaseModel
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.


def _ensure_env(var: str):
    if not os.environ.get(var):
        raise RuntimeError(f"{var} is not set. Please set it in your environment or .env file.")


_ensure_env("ANTHROPIC_API_KEY")

model = ChatAnthropic(temperature=0, model_name="claude-3-7-sonnet-latest")


@asynccontextmanager
async def get_tools():
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('NOSTR_CLIENT_PRIVATE_KEY')
    current_datetime_mcp_server_public_key = os.getenv('NOSTR_SERVER_PUBLIC_KEY')
    exchange_rate_mcp_server_public_key = os.getenv('NOSTR_SERVER_PUBLIC_KEY')
    math_mcp_server_public_key = os.getenv('NOSTR_SERVER_PUBLIC_KEY')
    nwc_str = os.getenv('NWC_CONN_STR')
    async with MultiServerMCPClient(
        {
            "current_datetime": {
                "relays": relays,
                "server_public_key": current_datetime_mcp_server_public_key,
                "private_key": private_key,
                "nwc_str": nwc_str,
                "transport": "nostr",
            },
            "exchange_rate": {
                "relays": relays,
                "server_public_key": exchange_rate_mcp_server_public_key,
                "private_key": private_key,
                "nwc_str": nwc_str,
                "transport": "nostr",
            },
            "math": {
                "relays": relays,
                "server_public_key": math_mcp_server_public_key,
                "private_key": private_key,
                "nwc_str": nwc_str,
                "transport": "nostr",
            },
        }
    ) as client:
        yield client.get_tools()


@asynccontextmanager
async def mcp_client():
    async with get_tools() as tools:
        agent = create_react_agent(model, tools, checkpointer=MemorySaver())
        yield agent


class Skill(BaseModel):
    """Skill to be used by the agent."""

    name: str
    description: str


class AgentInfo(BaseModel):
    """Agent information."""

    name: str
    description: str
    skills: list[Skill]
    satoshis: int
    nostr_pubkey: str


class ChatInput(BaseModel):
    messages: list[str]
    thread_id: str


app = FastAPI()


@app.get("/info")
async def info():
    async def get_skills():
        async with get_tools() as tools:
            return [Skill(
                    name=tool.name,
                    description=tool.description,
                ) for tool in tools]
    skills = await get_skills()
    return AgentInfo(
        name='Nostr MCP Agent',
        description=('This agent can check the current date and time, '
                     'perform basic mathematical operations, '
                     'and get the exchange rate between two currencies.'),
        skills=skills,
        satoshis=50,
        nostr_pubkey=PrivateKey.from_nsec(os.getenv('NOSTR_CLIENT_PRIVATE_KEY')).public_key.bech32(),
    ).model_dump()


@app.post("/chat")
async def chat(input: ChatInput):
    config = {"configurable": {"thread_id": input.thread_id}}
    async with mcp_client() as graph:
        response = await graph.ainvoke({"messages": input.messages}, config=config)
    return response["messages"][-1].content
