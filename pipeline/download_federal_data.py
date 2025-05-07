import aiohttp
import asyncio
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path("pipeline/data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://www.federalregister.gov/api/v1/documents.json"

async def fetch_documents(session, date):
    params = {
        "per_page": 100,
        "order": "newest",
        "conditions[publication_date][gte]": date
    }
    async with session.get(BASE_URL, params=params) as response:
        data = await response.json()
        return data["results"]

async def download():
    async with aiohttp.ClientSession() as session:
        today = datetime.today()
        since_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        documents = await fetch_documents(session, since_date)

        with open(DATA_DIR / f"federal_docs_{since_date}.json", "w") as f:
            json.dump(documents, f)
        print(f"Saved {len(documents)} documents.")

if __name__ == "__main__":
    asyncio.run(download())
