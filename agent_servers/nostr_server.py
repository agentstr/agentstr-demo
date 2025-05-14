import threading
from typing import Callable, Any
import json
import time
from pynostr.event import Event
import requests
from nostr_agents.nostr_agent_server import NostrAgentServer
from nostr_agents.nostr_client import NostrClient


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Get the environment variables
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('NOSTR_SERVER_PRIVATE_KEY')
    nwc_str = os.getenv('NWC_CONN_STR')
    agent_url = os.getenv('AGENT_URL')

    # Create an instance of NostrClient
    client = NostrClient(relays, private_key, nwc_str)
    server = NostrAgentServer("Distributed MCP Agent", agent_url, 0, client)
    server.start()
