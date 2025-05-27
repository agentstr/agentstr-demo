import os
import asyncio
from typing import Optional
from fastapi import FastAPI
from pynostr.key import PrivateKey
from pydantic import BaseModel
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient, NostrConnection
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from nostr_agents.nostr_client import NostrClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # take environment variables from .env.

model = ChatOpenAI(temperature=0, model_name="claude-3-7-sonnet-latest")
ml_models = {}


async def mcp_client():
    private_key = os.getenv('AGENT_PRIVATE_KEY')
    relays = os.getenv('NOSTR_RELAYS').split(',')
    nwc_str = os.getenv('AGENT_NWC_CONN_STR')
    nostr_client = NostrClient(relays, private_key, nwc_str)
    mcp_servers = await asyncio.to_thread(nostr_client.read_posts_by_tag,
                                          os.getenv('NOSTR_MCP_TOOL_DISCOVERY_TAG'))
    mcp_connections: dict[str, NostrConnection] = {
        mcp_server['pubkey']: NostrConnection(
            relays=[tag[1] for tag in mcp_server['tags'] if tag[0] == 'r'],
            server_public_key= mcp_server['pubkey'],
            private_key=private_key,
            nwc_str=nwc_str,
            transport="nostr",
        ) for mcp_server in mcp_servers
    }
    client = MultiServerMCPClient(mcp_connections)
    connections = client.connections or {}
    client.connections = connections
    for server_name, connection in connections.items():
        await client.connect_to_server(server_name, **connection)
    return client


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
    thread_id: Optional[str] = None



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    client = await mcp_client()
    tools = client.get_tools()
    agent = create_react_agent(model, tools, checkpointer=MemorySaver())
    skills = [Skill(
                name=tool.name,
                description=tool.description,
            ) for tool in tools]
    ml_models["agent"] = agent
    ml_models["skills"] = skills
    yield
    # Clean up the ML models and release the resources
    await client.exit_stack.aclose()
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/info")
async def info():
    return AgentInfo(
        name='Nostr MCP Agent',
        description=('This agent can check the current date and time, '
                     'perform basic mathematical operations, '
                     'and get the exchange rate between two currencies.'),
        skills=ml_models['skills'],
        satoshis=50,
        nostr_pubkey=PrivateKey.from_nsec(os.getenv('AGENT_PRIVATE_KEY')).public_key.bech32(),
    ).model_dump()


@app.post("/chat")
async def chat(input: ChatInput):
    config = {"configurable": {"thread_id": input.thread_id or str(uuid.uuid4())}}
    print(f'Found request: {input.messages[-1]}')
    response = await ml_models['agent'].ainvoke({"messages": input.messages[-1]}, config=config)
    return response["messages"][-1].content


if __name__ == '__main__':
    import uuid
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    async def run():
        client = await mcp_client()
        tools = client.get_tools()
        agent = create_react_agent(model, tools, checkpointer=MemorySaver())
        async for output in agent.astream({"messages": "what's the weather in portland?"}, stream_mode="updates", config=config):
            print(output)
        async for output in agent.astream({"messages": "what's the current date and time?"}, stream_mode="updates", config=config):
            print(output)

    asyncio.run(run())
