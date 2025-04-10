from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseMessage
from dotenv import load_dotenv
from app.graph import graph


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


@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    lc_messages = []
    for msg in chat_request.messages:
        lc_messages.append(
            (
                msg.type,
                msg.content
            )
        )
    response = []
    for s in graph.stream(
            {"messages": lc_messages}, subgraphs=True
    ):
        response.append(s)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
