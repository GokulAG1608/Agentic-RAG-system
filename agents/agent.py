import json
import aiohttp
import sys
import os

# Add the 'agents' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents')))

# Import your tool
from tools import fetch_documents_by_president

# Ollama LLM endpoint using Mistral
LLM_URL = "http://localhost:11434/v1/chat/completions"

# Tool registry
TOOLS = {
    "fetch_documents_by_president": fetch_documents_by_president
}

# Tool schema definition for LLM function calling
TOOL_SCHEMA = {
    "name": "fetch_documents_by_president",
    "description": "Get federal documents for a given US president.",
    "parameters": {
        "type": "object",
        "properties": {
            "president": {"type": "string", "description": "Name of the US president"}
        },
        "required": ["president"]
    }
}

# Agent function that handles user input and optionally uses tools
async def agent_respond(user_query: str):
    # Step 1: Send initial message to Mistral
    async with aiohttp.ClientSession() as session:
        payload = {
            "model": "mistral",  # or "mistral:7b" depending on your Ollama model name
            "messages": [{"role": "user", "content": user_query}],
            "tools": [TOOL_SCHEMA],
            "tool_choice": "auto",
            "stream": False
        }
        async with session.post(LLM_URL, json=payload) as res:
            output = await res.json()

    # Step 2: Check if tool is called
    message = output["choices"][0]["message"]
    if "tool_calls" in message:
        tool_call = message["tool_calls"][0]
        function_name = tool_call["function"]["name"]
        args = json.loads(tool_call["function"]["arguments"])

        # Step 3: Call the corresponding tool function
        tool_func = TOOLS[function_name]
        result = await tool_func(**args)

        # Step 4: Return tool output back to LLM to generate final response
        followup_payload = {
            "model": "mistral",
            "messages": [
                {"role": "user", "content": user_query},
                {"role": "assistant", "tool_calls": [tool_call]},
                {"role": "tool", "tool_call_id": tool_call["id"], "content": json.dumps(result)}
            ],
            "stream": False
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(LLM_URL, json=followup_payload) as res:
                final = await res.json()
        return final["choices"][0]["message"]["content"]

    # Step 5: If no tool is used, return LLM response directly
    return message["content"]

