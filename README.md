# Agentstr Demo

## Design and Build Nostr AI Agents 🤖⚡

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A decentralized AI agent system built on Nostr and Lightning Network, using the Agentstr SDK, featuring MCP servers and Langgraph agents.

## 🚀 Features

- 🤖 Langgraph Agents with MCP integration
- ⚡ Lightning Network payments via Nostr Wallet Connect
- 🌐 Decentralized communication using Nostr protocol
- 🧮 Built-in tools for math, exchange rates, and datetime queries
- 🔐 Secure, private key-based authentication

## 🛠️ Prerequisites

Before you begin, ensure you have the following:

- 🐍 Python 3.11 or higher
- 💎 `uv` package manager
- 📦 Dependencies from `pyproject.toml`:
  - `agentstr-sdk`
  - `pynostr`
  - `bolt11`
  - `fastapi`
  - `langchain`
  - And more...
- 🔑 A `.env` file with required environment variables
- 📡 Access to Nostr relays
- 💰 A Lightning wallet supporting NWC

## 🤖 Agent Server

### 1. `agent_servers/mcp_agent_api.py`
A FastAPI application providing an API for an MCP agent with tool integration.

- **Functionality**:
  - Initialize a `MultiServerMCPClient` to connect to MCP servers via Nostr.
  - Create a LangChain agent with tools using Anthropic's Claude model.
  - Expose endpoints:
    - `/info`: Returns agent information (name, description, skills, etc.).
    - `/chat`: Handles chat requests with optional thread IDs.
  - Manage lifecycle with async context (`lifespan`).
- **Usage**: Runs an API server for agent interactions.
- **Example**: Run the API:
  ```bash
  uv run uvicorn agent_servers.mcp_agent_api:app
  ```

### 2. `agent_servers/nostr_agent_listener.py`
A script to start a `NostrAgentServer` for listening to Nostr messages.

- **Functionality**:
  - Load environment variables and initialize a `NostrClient`.
  - Start a `NostrAgentServer` with a specified agent URL and satoshis cost.
- **Usage**: Entry point to run the agent server.
- **Example**: Run the listener:
  ```bash
  uv run agent_servers/nostr_agent_listener.py
  ```
  
## ⚡ MCP Servers

### 1. `mcp_servers/exchange_rate.py`
A script running an MCP server for exchange rate queries.

- **Functionality**:
  - Define a `get_exchange_rate` tool to fetch rates via the Frankfurter API.
  - Initialize a `NostrMCPServer` and add the tool with a 3-satoshi cost.
  - Start the server to handle requests.
- **Usage**: Provides exchange rate data over Nostr.
- **Example**: Query USD to EUR rate:
  ```json
  {"action": "call_tool", "tool_name": "get_exchange_rate", "arguments": {"currency_from": "USD", "currency_to": "EUR"}}
  ```

### 2. `mcp_servers/basic_math.py`
A script running an MCP server for basic math operations.

- **Functionality**:
  - Define tools for addition, multiplication, subtraction, and division.
  - Initialize a `NostrMCPServer` and add the tools.
  - Start the server to handle math requests.
- **Usage**: Provides math operations over Nostr.
- **Example**: Multiply two numbers:
  ```json
  {"action": "call_tool", "tool_name": "multiply", "arguments": {"a": 2, "b": 5}}
  ```

### 3. `mcp_servers/current_datetime.py`
A script running an MCP server for datetime queries.

- **Functionality**:
  - Define tools for current datetime, date, and time.
  - Initialize a `NostrMCPServer` and add the tools.
  - Start the server to handle datetime requests.
- **Usage**: Provides datetime information over Nostr.
- **Example**: Get current date:
  ```json
  {"action": "call_tool", "tool_name": "get_current_date", "arguments": {}}
  ```

## 🛠️ Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ehallmark/nostr-ai
   cd nostr-ai
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file with the following (example):
   ```env
    AGENT_PRIVATE_KEY=<nsec...>
    MCP_DATETIME_PRIVATE_KEY=<nsec...>
    MCP_EXCHANGE_RATE_PRIVATE_KEY=<nsec...>
    MCP_MATH_PRIVATE_KEY=<nsec...>
    NOSTR_RELAYS=wss://relay.primal.net,wss://relay.damus.io,wss://nostr.mom
    ANTHROPIC_API_KEY=<anthropic-api-key>
    AGENT_URL=http://127.0.0.1:8000
    AGENT_NWC_CONN_STR=<nostr+walletconnect://...>
    MCP_EXCHANGE_RATE_NWC_CONN_STR=<nostr+walletconnect://...>
    NOSTR_MCP_TOOL_DISCOVERY_TAG=mcp_tool_discovery
   ```
   
4. **Run the demo (each in its own terminal)**:

`./scripts/run_mcp_server_datetime.sh`

`./scripts/run_mcp_server_exchange_rate.sh`

`./scripts/run_mcp_server_math.sh`

`./scripts/run_mcp_agent_api.sh`

`./scripts/run_mcp_agent_listener.sh`

## ⚠️ Notes

- Each MCP Server requires its own Nostr private key
- Ensure Nostr relays are accessible and reliable.
- Payment-related operations require a valid NWC connection string.
- The `nostr_rag.py` server requires the agentstr-sdk package and its dependencies.
- The `mcp_agent_api.py` script requires an Anthropic API key for the Claude model.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.