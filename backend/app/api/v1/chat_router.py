import datetime

from uuid import UUID
from fastapi import APIRouter, Security, Depends, HTTPException, status
from app.checkpointer import get_checkpointer
from app.dependencies import get_graph
from langgraph.checkpoint.base import BaseCheckpointSaver
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.db.models import Session
from app.db.engine import get_db, AsyncSession
from app.core.auth import auth
from fastapi_auth0 import Auth0User
from sqlalchemy.future import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate


router = APIRouter(prefix="/chat", dependencies=[Security(auth.get_user)], tags=["Chat"])


@router.post("")
async def create_session(
        db: AsyncSession = Depends(get_db),
        user: Auth0User = Security(auth.get_user)
) -> str:
    new_session = Session(
        user_id=user.id
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return str(new_session.id)


class SessionOut(BaseModel):
    created_at: datetime.datetime
    id: UUID
    user_id: str
    name: str | None


@router.get("/sessions")
async def get_my_sessions(
        user: Auth0User = Security(auth.get_user),
        db: AsyncSession = Depends(get_db)
) -> Page[SessionOut]:
    return await paginate(
        db,
        select(Session)
        .filter(Session.user_id == user.id)
        .order_by(Session.created_at)
    )


@router.delete("/{session_id}")
async def delete_session(
        session_id: str,
        user: Auth0User = Security(auth.get_user),
        db: AsyncSession = Depends(get_db)
):
    stmt = select(Session).filter(Session.id == session_id, Session.user_id == user.id)
    result = await db.execute(stmt)
    session_to_delete = result.scalars().first()

    if not session_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found or you do not have perimssion to view"
        )

    await db.delete(session_to_delete)
    await db.commit()


@router.get("/{session_id}")
async def get_messages_for_session(
        session_id: str,
        memory: BaseCheckpointSaver = Depends(get_checkpointer)
):
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
