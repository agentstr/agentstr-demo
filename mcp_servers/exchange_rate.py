import httpx
from nostr_agents.nostr_client import NostrClient
from nostr_agents.nostr_mcp_server import NostrMCPServer


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Get the environment variables
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('MCP_EXCHANGE_RATE_PRIVATE_KEY')
    nwc_str = os.getenv('MCP_EXCHANGE_RATE_NWC_CONN_STR')


    def get_exchange_rate(
            currency_from: str = 'USD',
            currency_to: str = 'EUR',
            currency_date: str = 'latest',
    ):
        """Use this to get current exchange rate.

        Args:
            currency_from: The currency to convert from (e.g., "USD").
            currency_to: The currency to convert to (e.g., "EUR").
            currency_date: The date for the exchange rate or "latest". Defaults to "latest".

        Returns:
            A dictionary containing the exchange rate data, or an error message if the request fails.
        """
        try:
            response = httpx.get(
                f'https://api.frankfurter.app/{currency_date}',
                params={'from': currency_from, 'to': currency_to},
            )
            response.raise_for_status()

            data = response.json()
            if 'rates' not in data:
                print(f'rates not found in response: {data}')
                return {'error': 'Invalid API response format.'}
            print(f'API response: {data}')
            return data
        except httpx.HTTPError as e:
            print(f'API request failed: {e}')
            return {'error': f'API request failed: {e}'}
        except ValueError:
            print('Invalid JSON response from API')
            return {'error': 'Invalid JSON response from API.'}

    # Create an instance of NostrClient
    client = NostrClient(relays, private_key, nwc_str)
    server = NostrMCPServer("Exchange Rate MCP Server", client)
    server.add_tool(get_exchange_rate, satoshis=3)  # Specify price in satoshis

    server.start()

    '''
    {"action": "call_tool", "tool_name": "get_exchange_rate", "arguments": {"currency_from": "USD", "currency_to": "EUR"}}
    '''