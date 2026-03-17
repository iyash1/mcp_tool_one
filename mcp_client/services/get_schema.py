import json, httpx
from constants import MCP_BASE
from agents.mcp import MCPServerSse

mcp_tool = MCPServerSse({
    "name": "AI Tutor",
    "url": MCP_BASE,
    "timeout": 30,
    "client_session_timeout_seconds":60
})

client = httpx.Client()  # Create an HTTP client instance


def fetch_schema(server_url):
    """Fetches and parses the MCP schema from a server."""
    
    schema_url = server_url.replace("/sse", "/schema")
    print(f"Fetching schema from: {schema_url}")
    
    response = client.get(schema_url, timeout = 10)  # Add a timeout
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    schema_data = response.json()
    print("Schema fetched successfully!")
    return schema_data
    
    
def get_schema():
    print("--- Fetching AI Tutor Schema ---")
    tutor_schema = fetch_schema(MCP_BASE)

    if tutor_schema:
        print("\nAI Tutor Schema Contents:")
        # Pretty print the JSON manifest
        print(json.dumps(tutor_schema, indent=2))
        print("\n" + "=" * 50 + "\n")  # Separator
