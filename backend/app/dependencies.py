from fastapi import Depends
from app.checkpointer import get_checkpointer
from app.graph import create_graph


async def get_graph(checkpointer=Depends(get_checkpointer)):
    return create_graph(checkpointer)
