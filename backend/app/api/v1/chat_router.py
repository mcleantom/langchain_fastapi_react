from fastapi import APIRouter, Security, Depends, HTTPException, status
from app.core.auth import auth
from app.checkpointer import get_checkpointer
from app.dependencies import get_graph
from langgraph.checkpoint.base import BaseCheckpointSaver
from pydantic import BaseModel
from langchain_core.messages import HumanMessage


router = APIRouter(prefix="/chat", dependencies=[Security(auth.get_user)], tags=["Chat"])


@router.get("/{session_id}")
async def get_messages_for_session(session_id: str, memory: BaseCheckpointSaver = Depends(get_checkpointer)):
    messages = await memory.aget({"configurable": {"thread_id": session_id}})
    if messages is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Chat with session id {session_id} not found")
    return messages


class ChatRequest(BaseModel):
    message: str


@router.post("/{session_id}")
async def chat(session_id: str, message: ChatRequest, graph=Depends(get_graph)):
    config = {"configurable": {"thread_id": session_id}}
    response = []
    async for s in graph.astream(
        {"messages": [HumanMessage(content=message.message)]},
        subgraphs=True,
        config=config
    ):
        response.append(s)
    return response


