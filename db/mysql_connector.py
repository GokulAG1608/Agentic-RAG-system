import aiomysql
import asyncio
from typing import List, Dict, Any, Optional

class MySQLConnector:
    def __init__(self, host: str, port: int, user: str, password: str, db: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.pool: Optional[aiomysql.Pool] = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            autocommit=True,
            minsize=1,
            maxsize=5,
        )

    async def disconnect(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def fetch_all(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                result = await cur.fetchall()
                return result

    async def fetch_one(self, query: str, params: tuple = ()) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                result = await cur.fetchone()
                return result

    async def execute_query(self, query: str, params: tuple = ()) -> None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)

 