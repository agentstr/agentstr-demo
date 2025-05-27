from nostr_agents.nostr_agent_server import NostrAgentServer
from nostr_agents.nostr_client import NostrClient


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Get the environment variables
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('AGENT_PRIVATE_KEY')
    nwc_str = os.getenv('AGENT_NWC_CONN_STR')
    agent_url = os.getenv('AGENT_URL')

    # Create an instance of NostrClient
    client = NostrClient(relays, private_key, nwc_str)
    server = NostrAgentServer(agent_url, 5, client)
    server.start()
