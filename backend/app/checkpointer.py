import os
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver


DB_URI = os.environ["DB_URI"]
connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0
}

pool = None
checkpointer = None


async def get_checkpointer():
    global pool, checkpointer
    if pool is None or checkpointer is None:
        pool = AsyncConnectionPool(
            conninfo=DB_URI,
            max_size=20,
            kwargs=connection_kwargs
        )
        await pool.open(wait=True)
        checkpointer = AsyncPostgresSaver(pool)
        await checkpointer.setup()
    return checkpointer
