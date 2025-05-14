import time
from nostr_agents.nostr_client import NostrClient
from nostr_agents.nostr_mcp_server import NostrMCPServer


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Get the environment variables
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('MCP_DATETIME_PRIVATE_KEY')
    nwc_str = os.getenv('NWC_CONN_STR')

    def get_current_datetime() -> str:
        """Gets the current date and time"""
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def get_current_date() -> str:
        """Gets today's date"""
        return time.strftime("%Y-%m-%d")

    def get_current_time() -> str:
        """Gets the time of day"""
        return time.strftime("%H:%M:%S")

    # Create an instance of NostrClient
    client = NostrClient(relays, private_key, nwc_str)
    server = NostrMCPServer("Current Datetime Server", client)
    server.add_tool(get_current_datetime)
    server.add_tool(get_current_date)
    server.add_tool(get_current_time)

    server.start()

    '''
    {"action": "call_tool", "tool_name": "get_current_date", "arguments": {}}
    '''