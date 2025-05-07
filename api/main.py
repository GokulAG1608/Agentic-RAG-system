# File: api/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from agents.agent import agent_respond

app = FastAPI()

# Enable CORS for all origins (for dev use only; restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "RAG Agent is running!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("query")
    if not user_input:
        return {"error": "No query provided"}
    
    response = await agent_respond(user_input)
    return {"response": response}


# Use this only when running as a script: `python api/main.py`
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
