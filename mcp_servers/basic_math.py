from nostr_agents.nostr_mcp_server import NostrMCPServer, NostrClient


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Get the environment variables
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('MCP_MATH_PRIVATE_KEY')
    nwc_str = os.getenv('NWC_CONN_STR')


    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    def multiply(a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b

    def subtract(a: int, b: int) -> int:
        """Subtract two numbers"""
        return a - b

    def divide(a: int, b: int) -> int:
        """Divide two numbers (integer division)"""
        return a // b

    # Create an instance of NostrClient
    client = NostrClient(relays, private_key, nwc_str)
    server = NostrMCPServer("Math MCP Server", client)
    server.add_tool(add)  # Add by signature alone
    server.add_tool(multiply, name="multiply", description="Multiply two numbers")  # Add by signature and name
    server.add_tool(subtract)
    server.add_tool(divide)

    server.start()

    '''
    {"action": "call_tool", "tool_name": "add", "arguments": {"a": 1, "b": 2}}
    {"action": "call_tool", "tool_name": "multiply", "arguments": {"a": 2, "b": 5}}
    '''