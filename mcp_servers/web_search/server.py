import os
from tavily import TavilyClient


def web_search(query: str, num_results: int = 10) -> dict:
    """
    Search the web using Tavily Search API.

    Args:
        query: Search query string
        num_results: Number of results to return (default: 10)

    Returns:
        A dictionary containing search results
    """
    # Get the Tavily API key from environment variables
    tavily_api_key = os.getenv('TAVILY_API_KEY')
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY environment variable not set")

    try:
        # Initialize Tavily client
        tavily_client = TavilyClient(api_key=tavily_api_key)
        
        # Perform the search
        results = tavily_client.search(query, num_results=num_results).get('results', [])
        
        # Format results for MCP
        formatted_results = {
            "query": query,
            "num_results": num_results,
            "results": [
                {
                    "title": result.get('title', ''),
                    "content": result.get('content', ''),
                    "url": result.get('url', ''),
                    "snippet": result.get('snippet', ''),
                    "domain": result.get('domain', ''),
                    "rank": result.get('rank', 0)
                }
                for result in results
            ]
        }
        
        return formatted_results
    
    except Exception as e:
        return {
            "error": f"Search failed: {str(e)}"
        }


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from agentstr import NostrMCPServer

    load_dotenv()

    # Get the environment variables
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('MCP_SERVER_PRIVATE_KEY')
    nwc_str = os.getenv('MCP_SERVER_NWC_CONN_STR')

    # Create the MCP server
    server = NostrMCPServer(
        "Web Search Tool",
        relays=relays,
        private_key=private_key,
        nwc_str=nwc_str,
    )

    server.add_tool(web_search,
                    satoshis=10)

    # Start the server
    server.start()
