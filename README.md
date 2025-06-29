# DEPRECATED

See https://github.com/agentstr/agentstr-sdk/main/main/cookbook for the latest Agentstr Demo code.

# DEPRECATED

# Agentstr Demo

## A Decentralized AI Gig Economy

### See the demo in action [here](https://agentstr.com/demo).


[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### What is Agentstr?

Agentstr is a framework for building decentralized AI agents on the Nostr protocol, featuring LangChain and DSPy integrations, with Lightning Network payments via Nostr Wallet Connect.

## 🚀 Features

- 🤖 Multiple Agent Backends
  - Research Agent: Langgraph-based agent with Nostr MCP server integration
  - Travel Agent: DSPy-based agent for flight booking and management
- ⚡ Lightning Network payments via Nostr Wallet Connect
- 🌐 Decentralized communication using Nostr protocol
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
- 🔑 Several `.env` files with required environment variables- 📡 Access to Nostr relays
- 💰 A Lightning wallet supporting NWC

## 🤖 Agents

### 1. Research Agent 

[agents/research/agent.py](agents/research/agent.py)

We define a Langgraph-based agent with MCP server integration for general research tasks.

- **Functionality**:
  - Initializes a `MultiServerMCPClient` to connect to MCP servers via Nostr
  - Starts a `NostrAgentServer` for listening to Nostr messages
  - Exposes endpoints:
    - `/info`: Returns agent information (name, description, skills, etc.)
    - `/chat`: Handles chat requests with optional thread IDs
  - Manages lifecycle with async context (`lifespan`)
- **Usage**: Run the research agent API server:
  ```bash
  ./scripts/run_agent_research.sh
  ```

### 2. Travel Agent 

[agents/travel/agent.py](agents/travel/agent.py)

A DSPy-based agent specialized in flight booking and management.

- **Functionality**:
  - Manages flight bookings, cancellations, and itinerary lookups
  - Integrates with a simulated flight database
  - Provides a simple API endpoint for interactions
  - Uses DSPy for natural language understanding and task planning
- **Features**:
  - Flight search and booking
  - Itinerary management
  - Flight cancellation
  - User profile integration
- **Usage**: Run the travel agent server:
  ```bash
  ./scripts/run_agent_travel.sh
  ```

## ⚡ MCP Servers

#### 1. [mcp_servers/bitcoin/server.py](mcp_servers/bitcoin/server.py)
A script running an MCP server for Bitcoin-related queries.

- **Functionality**:
  - Provides tools for Bitcoin price queries and blockchain information.
  - Initialize a `NostrMCPServer` with Bitcoin-specific tools.
  - Start the server to handle Bitcoin-related requests.
- **Usage**: Provides Bitcoin price and blockchain data over Nostr.
- **Example**: Query current Bitcoin price:
  ```json
  {"action": "call_tool", "tool_name": "get_bitcoin_data", "arguments": {}}
  ```

#### 2. [mcp_servers/nostr_rag/server.py](mcp_servers/nostr_rag/server.py)
A script running an MCP server for Nostr RAG (Retrieval-Augmented Generation).

- **Functionality**:
  - Provides tools for semantic search over Nostr content.
  - Implements vector embeddings and similarity search for Nostr events.
  - Initialize a `NostrMCPServer` with RAG tools.
  - Start the server to handle semantic search requests.
- **Usage**: Enables semantic search over Nostr content.
- **Example**: Search for similar content:
  ```json
  {"action": "call_tool", "tool_name": "retrieve", "arguments": {"question": "what's new with bitcoin?"}}
  ```

#### 3. [mcp_servers/web_search/server.py](mcp_servers/web_search/server.py)
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
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Copy the `.env.sample` file to `.env` in each agent directory
   - Update the environment variables with your configuration

4. **Run MCP Servers**:
   ```bash
   # In separate terminals
   ./scripts/run_mcp_server_bitcoin.sh
   ./scripts/run_mcp_server_nostr_rag.sh
   ./scripts/run_mcp_server_web_search.sh
   ```

5. **Run the Agents**:

   For the Research Agent:
   ```bash
   ./scripts/run_agent_research.sh
   ```

   For the Travel Agent:
   ```bash
   ./scripts/run_agent_travel.sh
   ```


## ⚠️ Notes

- Each Agent and MCP Server requires its own Nostr private key and environment variables (see .env.sample files in each directory)
- Ensure Nostr relays are accessible and reliable.
- Payment-related operations require a valid NWC connection string.
- Both agents and the RAG MCP server require an LLM API key and base url (checkout [Routstr](https://routstr.com) for decentralized LLM access).

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
