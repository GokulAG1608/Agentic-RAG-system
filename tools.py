import aiomysql
import os

async def fetch_documents_by_president(president: str):
    conn = await aiomysql.connect(
        host="localhost", port=3306,
        user="root", password="root@1234",
        db="ragdb"
    )
    cur = await conn.cursor()
    await cur.execute("SELECT title, summary FROM federal_documents WHERE president LIKE %s", (f"%{president}%",))
    rows = await cur.fetchall()
    await cur.close()
    conn.close()
    return [{"title": r[0], "summary": r[1]} for r in rows]
