Async RAG Agentic System with Daily-Updated MySQL Pipeline
This project is a Retrieval-Augmented Generation (RAG) system that allows users to interact with a local LLM agent (via Ollama or OpenAI-compatible APIs) through a simple chat interface. The LLM uses pre-defined tools to fetch answers from a daily-updating MySQL database, powered by an automated data pipeline.

📌 Features
✅ Daily-updated data pipeline (e.g., Federal Register or FDA API)

✅ MySQL database for structured data storage and querying

✅ Async Python for non-blocking execution (LLM inference, DB access, API calls)

✅ LLM with Agentic Tool Calling

✅ Simple UI (HTML/JS) or Streamlit interface

✅ Barebones FastAPI or WebSocket based API to interact with LLM

✅ Compatible with local models like qwen:0.5b or qwen:1b via Ollama

🧱 System Architecture
mermaid
Copy
Edit
graph TD
    A[Data Source API (e.g. Federal Register)] --> B[Data Pipeline]
    B --> C[MySQL Database]

    D[User Input via UI/API] --> E[Agent/LLM]
    E -->|Tool Call| F[MySQL Tool Function]
    F --> C
    C --> F
    F -->|Result| E
    E -->|Response| D
🛠️ Tech Stack
Component	Tech
LLM	Ollama (Qwen 0.5B/1B), OpenAI-compatible
Backend API	FastAPI or WebSockets
Data Pipeline	Python + aiohttp, aiofiles
Database	MySQL (Raw SQL queries only)
Async DB Access	aiomysql
UI (Optional)	HTML/CSS/JS or Streamlit

📂 Project Structure
bash
Copy
Edit
.
├── app/
│   ├── agent.py              # Agent logic with tool function schema
│   ├── tools.py              # Tool functions for DB interaction
│   ├── pipeline/
│   │   ├── fetch_data.py     # Async data fetcher from public API
│   │   ├── process_data.py   # Cleans and transforms data
│   │   └── upload_mysql.py   # Inserts cleaned data into MySQL
│   ├── api.py                # FastAPI server or WebSocket logic
│   └── utils/
│       └── db.py             # Async DB connector using aiomysql
├── templates/
│   └── index.html            # Simple UI (Optional)
├── requirements.txt
└── README.md
🚀 Getting Started
1. Clone the Repository
bash
Copy
Edit
git clone (https://github.com/GokulAG1608/Agentic-RAG-system.git)
cd async-agentic-rag
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Start MySQL and Create Tables
Ensure MySQL is running and create the required database and tables.

sql
Copy
Edit
CREATE DATABASE rag_agent;

-- Example Table (adjust as per your data schema)
CREATE TABLE executive_documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title TEXT,
    summary TEXT,
    date DATE,
    president VARCHAR(255)
);
4. Run Data Pipeline
bash
Copy
Edit
python app/pipeline/fetch_data.py
python app/pipeline/process_data.py
python app/pipeline/upload_mysql.py
5. Start the LLM via Ollama
bash
Copy
Edit
ollama run qwen:0.5b
Or set up your OpenAI-compatible endpoint in .env.

6. Run the Backend API
bash
Copy
Edit
uvicorn app.api:app --reload
7. Access UI (Optional)
Open your browser at http://localhost:8000.

🧪 Example User Queries
"What are the latest executive orders by Joe Biden from this week?"

"Summarize documents related to Artificial Intelligence from January 2025."

⚙️ Configurations
Create a .env file:

ini
Copy
Edit
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=rag_agent
OLLAMA_BASE_URL=http://localhost:11434/v1
✅ To-Do / Enhancements
 Add more tool functions (date filtering, search)

 Improve summarization quality

 Integrate logging (Optional)

 Extend to FDA dataset

❗ Guidelines Followed
✅ All tool calls are hidden from user

✅ No static data – data updates daily

✅ No code interpreter – only tool functions

✅ LLM can’t directly call API – must go through MySQL/tool

