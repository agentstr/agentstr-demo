from agentstr import NostrMCPClient
from pynostr.key import PrivateKey
import os
import json
import dotenv

dotenv.load_dotenv()

# Define relays and private key
relays = os.getenv('NOSTR_RELAYS').split(',')
private_key = PrivateKey().bech32()

# Define MCP server public key
server_public_key = 'npub1m7kklaydljpjscl37xpdgtzfs66u70t5aex68pgdnsmjcx0vllrsmxl6vk'

# Initialize the client
mcp_client = NostrMCPClient(mcp_pubkey=server_public_key, relays=relays, private_key=private_key)

# List available tools
tools = mcp_client.list_tools()
print(f'Found tools: {json.dumps(tools, indent=4)}')

# Call a tool
result = mcp_client.call_tool("get_bitcoin_data", {})
print(result)