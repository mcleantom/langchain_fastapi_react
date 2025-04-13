import os
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.memory import InMemorySaver
from functools import lru_cache
from app.core.config import settings


DB_URI = settings.postgres_database_uri
connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0
}

pool = None
checkpointer = None


@lru_cache()
def get_checkpointer():
    return InMemorySaver()


# async def get_checkpointer():
#     global pool, checkpointer
#     if pool is None or checkpointer is None:
#         pool = AsyncConnectionPool(
#             conninfo=DB_URI,
#             max_size=20,
#             kwargs=connection_kwargs
#         )
#         await pool.open(wait=True)
#         checkpointer = AsyncPostgresSaver(pool)
#         await checkpointer.setup()
#     return checkpointer
