import json
import os
import mysql.connector
from pathlib import Path
from datetime import datetime,timedelta

RAW_FILE = "pipeline/data/raw/federal_docs_{}.json"
DATE = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

def insert_to_mysql(docs):
    conn = mysql.connector.connect(
        host="localhost", user="root", password="password", database="ragdb"
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS federal_documents (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title TEXT,
            publication_date DATE,
            president TEXT,
            summary TEXT
        )
    """)

    for doc in docs:
        cursor.execute("""
            INSERT INTO federal_documents (title, publication_date, president, summary)
            VALUES (%s, %s, %s, %s)
        """, (
            doc.get("title", ""),
            doc.get("publication_date", ""),
            doc.get("president", ""),
            doc.get("summary", "")
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data inserted into MySQL.")

def process():
    with open(RAW_FILE.format(DATE), "r") as f:
        docs = json.load(f)
    insert_to_mysql(docs)

if __name__ == "__main__":
    process()
