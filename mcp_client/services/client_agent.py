# Let's Build the AI agent
from agents import Agent, Runner
from agents.mcp import MCPServerSse

from constants import MCP_BASE, MODEL_NAME

# timeout: 30
# This controls how long (in seconds) the server waits for a single tool execution (i.e., an action call) before giving up.

# client_session_timeout_seconds: 60
# This sets how long an entire client session is kept alive without activity before it's considered expired or disconnected.
# If the client doesn’t send any requests or interact for 60 seconds, the session times out.

mcp_tool = MCPServerSse({
    "name": "AI Tutor",
    "url": MCP_BASE,
    "timeout": 30,
    "client_session_timeout_seconds":60
})

agent = Agent(
    name = "Smart Assistant",
    instructions = """
    Context
    -------
    You are an AI assistant with access to an MCP server exposing **four streaming tools**:

    1. **explain_concept**  
    Arguments: { "question": <str>, "level": <int 1‑5> }  
    • Streams an explanation of any concept at the requested depth.

    2. **summarize_text**  
    Arguments: { "text": <str>, "compression_ratio": <float 0.1‑0.8> }  
    • Streams a concise summary ~compression_ratio × original length.

    3. **generate_flashcards**  
    Arguments: { "topic": <str>, "num_cards": <int 1‑20> }  
    • Streams JSON‑lines flashcards: one card per line `{ "q":…, "a":… }`.

    4. **quiz_me**  
    Arguments: { "topic": <str>, "level": <int 1‑5>, "num_questions": <int 1‑15> }  
    • Streams an MC‑question quiz, then an ANSWER KEY section.

    Objective
    ---------
    Help users learn by:
    • Explaining concepts at the depth they request.  
    • Summarising long passages.  
    • Generating flashcards for self‑study.  
    • Quizzing them interactively.

    How to respond
    --------------
    • For each user request, decide which tool (if any) fulfils it best.  
    • Call the tool via MCP by returning *only* the JSON with `"tool"` and `"arguments"` (no extra text).  
    • If a follow‑up conversation is needed (e.g., clarification), ask the user first.  
    • If no tool fits, answer directly in plain language.

    Examples
    --------
    User: “Explain quantum tunnelling like I’m 10.”  
    → Call `explain_concept` with { "question": "quantum tunnelling", "level": 2 }

    User: “Summarise this article to 20 %.” + <article text>  
    → Call `summarize_text` with { "text": "...", "compression_ratio": 0.2 }

    Chat capability
    ---------------
    After each tool call completes (streaming back to the user), remain in the chat loop ready for the next user turn.
    """,
    model = MODEL_NAME,
    mcp_servers = [mcp_tool],
)

async def call_services():
    try:
        connection_result = await mcp_tool.connect()  # open SSE channels
        print(f"Connected to MCP Server: {connection_result}")

        result = None
        while True:
            user_input = input("User: ")
            if user_input.lower() in {"exit", "quit"}:
                break
                
            # If there was a previous interaction (result is not None), it appends the new user message to the past messages (maintaining conversation context).
            if result is not None:
                new_input = result.to_input_list() + [{"role": "user", "content": user_input}]
            else:
                new_input = [{"role": "user", "content": user_input}]
            print("\nUser Input:")
            print(user_input)

            
            # This is the core AI agent execution step. It runs your agent with the new_input.

            result = await Runner.run(starting_agent = agent, input = new_input)
            print("\nAssistant:")
            print(result.final_output)
    except Exception as e:
        print(f"MCP Client Error: Unable to connect to tools \n {e}")