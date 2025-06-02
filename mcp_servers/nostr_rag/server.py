from dotenv import load_dotenv

load_dotenv()

import os
from agentstr import NostrMCPServer
from agentstr import NostrRAG

# Get the environment variables
relays = os.getenv('NOSTR_RELAYS').split(',')
private_key = os.getenv('MCP_SERVER_PRIVATE_KEY')
nwc_str = os.getenv('MCP_SERVER_NWC_CONN_STR')
llm_base_url = os.getenv('LLM_BASE_URL')
llm_api_key = os.getenv('LLM_API_KEY')
llm_model_name = os.getenv('LLM_MODEL_NAME')

# Initialize NostrRAG
nostr_rag = NostrRAG(
    relays=relays,
    private_key=private_key,
    llm_base_url=llm_base_url,
    llm_api_key=llm_api_key,
    llm_model_name=llm_model_name
)

async def nostr_search(query: str, num_results: int = 10) -> list[str]:
    """
    Search and retrieve content from Nostr using RAG.

    Args:
        query: Search query string
        num_results: Number of results to return (default: 10)

    Returns:
        A list of strings containing the retrieved content
    """
    return [doc.page_content for doc in await nostr_rag.retrieve(query, num_results=num_results)]


async def run():
    # Create the MCP server
    server = NostrMCPServer(
        "Nostr RAG Tool",
        relays=relays,
        private_key=private_key,
        nwc_str=nwc_str,
    )
    server.add_tool(nostr_search,
                    satoshis=10)
    # Start the server
    await server.start()


if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
 



