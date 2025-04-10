from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from langchain.schema import BaseMessage
from dotenv import load_dotenv
from app.dependencies import get_graph
from app.checkpointer import get_checkpointer
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
import asyncio
import sys

if sys.platform == 'win32':
    # Set the policy to prevent "Event loop is closed" error on Windows - https://github.com/encode/httpx/issues/914
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


load_dotenv()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[BaseMessage]


@app.get("/chat/{chat_id}")
async def get_chat_history(chat_id: str, memory: AsyncPostgresSaver = Depends(get_checkpointer)):
    messages = await memory.aget({"configurable": {"thread_id": chat_id}})
    return messages


@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest, graph=Depends(get_graph)):
    config = {"configurable": {"thread_id": "duasdhkjasd"}}
    lc_messages = []
    for msg in chat_request.messages:
        lc_messages.append(
            (
                msg.type,
                msg.content
            )
        )
    response = []
    async for s in graph.astream(
            {"messages": lc_messages}, subgraphs=True, config=config
    ):
        response.append(s)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
