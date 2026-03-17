
# 🤖 MCP Tool One

## Overview
AI Tutor — a small demo project that exposes four streaming MCP tools (explain, summarize, flashcards, quiz) via a Gradio-based MCP server and an interactive MCP client.

This repository contains two main parts:
- The MCP server (web UI + streaming tools): [mcp_server/app.py](mcp_server/app.py)
- The MCP client (interactive CLI to call the server): [mcp_client/app.py](mcp_client/app.py)

## Requirements
- Python 3.10+
- See [requirements.txt](requirements.txt) for pinned packages. Key dependencies:
  - `gradio` (web UI / MCP server)
  - `openai` (official client used to call models)
  - `python-dotenv` (load `.env`)
  - `colorama` (colored CLI output)
  - `httpx` (HTTP client used by `get_schema`)

Install with:

```bash
python -m pip install -r requirements.txt
```

## Environment
Copy or create a `.env` file in the repository root and set your OpenAI API key:

```bash
# Example .env
OPENAI_API_KEY=sk-...
```

The server and client read `OPENAI_API_KEY` from the environment (see [mcp_server/common/init_client.py](mcp_server/common/init_client.py) and [mcp_client/app.py](mcp_client/app.py)).

## Quick Start — Run locally
1. Install dependencies (see above).
2. Start the MCP server (launches a Gradio app exposing the tools):

```bash
python -m mcp_server.app
# or
python mcp_server/app.py
```

3. In a separate terminal, run the MCP client CLI to interact with the server:

```bash
python -m mcp_client.app
# or
python mcp_client/app.py
```

Notes:
- By default the client uses a remote `MCP_BASE` URL in [mcp_client/constants.py](mcp_client/constants.py). To test against a locally running server change `MCP_BASE` to `http://localhost:7860/gradio_api/mcp/sse`.
- The Gradio server launched by [mcp_server/app.py](mcp_server/app.py) runs on port 7860 by default.

## Useful commands
- Fetch the server schema (client helper):

```bash
python -m mcp_client.services.get_schema
```

- Run the interactive client to call tools: select option `2` in the menu.

## Project Layout
```
mcp_tool_one/
├── mcp_server/                 # Gradio server + streaming tool implementations
│   ├── app.py                  # Gradio app exposing tools
│   ├── constants.py            # server constants (MODEL_NAME, levels)
│   └── common/                 # helpers (init_client, style print)
│   └── tools/                  # explanation, summarization, flashcards, quiz
├── mcp_client/                 # Simple client to connect to MCP server
│   ├── app.py                  # CLI interactive client
│   ├── constants.py            # MCP_BASE and MODEL_NAME for client
│   └── services/               # client helpers (get_schema, client_agent)
├── .env                       # environment variables (not committed in prod)
├── requirements.txt           # Python dependencies
└── README.md
```

## Testing / Verification
1. Ensure `.env` has a valid `OPENAI_API_KEY`.
2. Start the server and visit the Gradio UI (http://localhost:7860/) — verify the four tabs work.
3. Run the client, choose `1` to fetch schema (verifies HTTP connectivity), then choose `2` to interact with tools via SSE.

## Troubleshooting
- Missing API key: both server and client will raise an error if `OPENAI_API_KEY` is not set.
- If streaming responses hang, check network connectivity and that `MCP_BASE` points to the running server.

## Contributing
PRs and issues welcome — please include clear reproduction steps.

## License
Add a license file or text here.
