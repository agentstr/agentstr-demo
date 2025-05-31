import os
import time
import asyncio
from agentstr.nostr_agent_server import NoteFilters
from pynostr.key import PrivateKey
from langchain_mcp_adapters.client import MultiServerMCPClient, NostrConnection
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from agentstr import NostrClient, NostrAgentServer, AgentCard, Skill, ChatInput
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


# Get the environment variables
relays = os.getenv('NOSTR_RELAYS').split(',')
private_key = os.getenv('AGENT_PRIVATE_KEY')
nwc_str = os.getenv('AGENT_NWC_CONN_STR')
agent_url = os.getenv('AGENT_URL')


model = ChatOpenAI(temperature=0,
                   base_url=os.getenv('LLM_BASE_URL'),
                   api_key=os.getenv('LLM_API_KEY'),
                   model_name=os.getenv('LLM_MODEL_NAME'))


def mcp_client():
    nostr_client = NostrClient(relays, private_key, nwc_str)
    mcp_servers = nostr_client.read_posts_by_tag(os.getenv('NOSTR_MCP_TOOL_DISCOVERY_TAG'))
    mcp_connections: dict[str, NostrConnection] = {
        mcp_server.pubkey: NostrConnection(
            relays=relays, #[tag[1] for tag in mcp_server.tags if tag[0] == 'r'],
            server_public_key=mcp_server.pubkey,
            private_key=private_key,
            nwc_str=nwc_str,
            transport="nostr",
        ) for mcp_server in mcp_servers
    }
    client = MultiServerMCPClient(mcp_connections)
    for server_name, connection in client.connections.items():
        client.connect_to_server(server_name, **connection)
    return client


if __name__ == "__main__":
    def run():
        # Load the ML model
        client = mcp_client()
        tools = client.get_tools()
        agent = create_react_agent(model, tools, checkpointer=MemorySaver())
        skills = [Skill(
            name=tool.name,
            description=tool.description,
            satoshis=tool.metadata.get("satoshis", 0),
        ) for tool in tools]

        agent_info = AgentCard(
            name='Research Agent',
            description=('This agent can query bitcoin blockchain data, '
                        'and perform web search.'),
            skills=skills,
            satoshis=5,
            nostr_pubkey=PrivateKey.from_nsec(os.getenv('AGENT_PRIVATE_KEY')).public_key.bech32(),
            nostr_relays=relays,
        )

        note_filters = NoteFilters(
            nostr_pubkeys=['npub1jch03stp0x3fy6ykv5df2fnhtaq4xqvqlmpjdu68raaqcntca5tqahld7a'],
        )

        def agent_callable(input: ChatInput) -> str:
            config = {"configurable": {"thread_id": input.thread_id or str(uuid.uuid4())}}
            print(f'Found request: {input.messages[-1]}')
            result = asyncio.run(agent.ainvoke({"messages": input.messages[-1]}, config=config))
            return result["messages"][-1].content

        server = NostrAgentServer(relays=relays,
                                  private_key=private_key,
                                  nwc_str=nwc_str,
                                  note_filters=note_filters,
                                  agent_info=agent_info,
                                  agent_callable=agent_callable,
                                  router_llm=lambda message: model.invoke(message).content)

        print(f"Starting nostr agent server...")
        server.start()

    #import asyncio
    #asyncio.run(run())
    run()