from fastapi import FastAPI, Depends, HTTPException, status, Security
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.dependencies import get_graph
from app.checkpointer import get_checkpointer
from langgraph.checkpoint.base import BaseCheckpointSaver
from langchain_core.messages import HumanMessage
import asyncio
import sys
import contextlib
from app.db.engine import session_manager
from app.core.auth import auth


if sys.platform == 'win32':
    # Set the policy to prevent "Event loop is closed" error on Windows - https://github.com/encode/httpx/issues/914
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


load_dotenv()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if session_manager._engine is not None:
        await session_manager.close()



app = FastAPI(lifespan=lifespan, title="LangchainAPI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/api/private")
def private(auth_result: str = Security(auth.verify)):
    return auth_result


@app.get("/chat/{thread_id}")
async def get_chat_history(thread_id: str, memory: BaseCheckpointSaver = Depends(get_checkpointer)):
    messages = await memory.aget({"configurable": {"thread_id": thread_id}})
    if messages is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Chat with thread_id {thread_id} not found")
    return messages


class ChatRequest(BaseModel):
    message: str


@app.post("/chat/{thread_id}")
async def chat(chat_request: ChatRequest, thread_id: str, graph=Depends(get_graph)):
    config = {"configurable": {"thread_id": thread_id}}
    response = []
    async for s in graph.astream(
        {"messages": [HumanMessage(content=chat_request.message)]},
        subgraphs=True,
        config=config
    ):
        response.append(s)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
