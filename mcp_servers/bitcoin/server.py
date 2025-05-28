import requests


BASE_URL = 'https://blockchain.info/q'


def get_24hr_price() -> str:
    """24 hour weighted price from the largest exchanges"""
    return requests.get(f'{BASE_URL}/24hrprice').text

def get_market_cap() -> str:
    """USD market cap (based on 24 hour weighted price)"""
    return requests.get(f'{BASE_URL}/marketcap').text
    
def get_24hr_transaction_count() -> str:
    """Number of transactions in the last 24 hours"""
    return requests.get(f'{BASE_URL}/24hrtransactioncount').text

def get_24hr_btc_sent() -> str:
    """Number of BTC sent in the last 24 hours"""
    return requests.get(f'{BASE_URL}/24hrbtcsent').text

def get_hashrate() -> str:
    """Current hashrate in GH/s"""
    return requests.get(f'{BASE_URL}/hashrate').text

def get_difficulty() -> str:
    """Current difficulty"""
    return requests.get(f'{BASE_URL}/getdifficulty').text

def get_block_count() -> str:
    """Current block count"""
    return requests.get(f'{BASE_URL}/getblockcount').text


def get_bitcoin_data() -> dict:
    return {
        "24hr_price": get_24hr_price(),
        "market_cap": get_market_cap(),
        "24hr_transaction_count": get_24hr_transaction_count(),
        "24hr_btc_sent": get_24hr_btc_sent(),
        "hashrate": get_hashrate(),
        "difficulty": get_difficulty(),
        "block_count": get_block_count(),
    }



if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from agentstr import NostrMCPServer

    load_dotenv()

    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('MCP_SERVER_PRIVATE_KEY')

    server = NostrMCPServer("Bitcoin Data Tool", relays=relays, private_key=private_key)

    server.add_tool(get_bitcoin_data)

    server.start()
    