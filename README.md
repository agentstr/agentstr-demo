# Agentstr Demo

### See the demo in action [here](https://agentstr.com/demo)

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

### 1. `agent_servers/agent_api.py`
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
  uv run uvicorn agent_servers.agent_api:app
  ```

### 2. `agent_servers/nostr_listener.py`
A script to start a `NostrAgentServer` for listening to Nostr messages.

- **Functionality**:
  - Load environment variables and initialize a `NostrClient`.
  - Start a `NostrAgentServer` with a specified agent URL and satoshis cost.
- **Usage**: Entry point to run the agent server.
- **Example**: Run the listener:
  ```bash
  uv run agent_servers/nostr_listener.py
  ```
  
## ⚡ MCP Servers

### 1. `mcp_servers/bitcoin/server.py`
A script running an MCP server for Bitcoin-related queries.

- **Functionality**:
  - Provides tools for Bitcoin price queries and blockchain information.
  - Initialize a `NostrMCPServer` with Bitcoin-specific tools.
  - Start the server to handle Bitcoin-related requests.
- **Usage**: Provides Bitcoin price and blockchain data over Nostr.
- **Example**: Query current Bitcoin price:
  ```json
  {"action": "call_tool", "tool_name": "get_market_cap", "arguments": {}}
  ```

### 2. `mcp_servers/nostr_rag/server.py`
A script running an MCP server for Nostr RAG (Retrieval-Augmented Generation).

- **Functionality**:
  - Provides tools for semantic search over Nostr content.
  - Implements vector embeddings and similarity search for Nostr events.
  - Initialize a `NostrMCPServer` with RAG tools.
  - Start the server to handle semantic search requests.
- **Usage**: Enables semantic search over Nostr content.
- **Example**: Search for similar content:
  ```json
  {"action": "call_tool", "tool_name": "retrieve", "arguments": {"question": "bitcoin price prediction"}}
  ```

### 3. `mcp_servers/web_search/server.py`
A script running an MCP server for web search capabilities.

- **Functionality**:
  - Provides tools for searching the web using a search engine API.
  - Initialize a `NostrMCPServer` with web search tools.
  - Start the server to handle web search requests.
- **Usage**: Enables web search capabilities over Nostr.
- **Example**: Perform a web search:
  ```json
  {"action": "call_tool", "tool_name": "web_search", "arguments": {"query": "latest AI developments"}}
  ```

## 🛠️ Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ehallmark/agentstr-demo
   cd agentstr-demo
   ```

2. **Install Dependencies**:
   ```bash
   uv sync
   ```

3. **Configure Environment Variables**:

   Create a `.env` file in each directory following the .env.sample files.
   
4. **Run the demo (each in its own terminal)**:

`./scripts/run_mcp_server_bitcoin.sh`

`./scripts/run_mcp_server_nostr_rag.sh`

`./scripts/run_mcp_server_web_search.sh`

`./scripts/run_agent_api.sh`

`./scripts/run_agent_listener.sh`

## ⚠️ Notes

- Each MCP Server requires its own Nostr private key and environment variables (see .env.sample files in each directory)
- Ensure Nostr relays are accessible and reliable.
- Payment-related operations require a valid NWC connection string.
- The `agent_api.py` and `nostr_rag.py` scripts require an LLM API Key and base url (checkout [routstr](https://routstr.com) for decentralized LLM access).

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.