from fastapi import FastAPI, WebSocket, Depends
from fastapi.responses import HTMLResponse
from app.graph import get_graph
from app.template import html
from pydantic import BaseModel


app = FastAPI()


class ChatInput(BaseModel):
    messages: list[str]
    thread_id: str


@app.post("/chat")
async def chat(chat_input: ChatInput, graph=Depends(get_graph)):
    config = {"configurable": {"thread_id": chat_input.thread_id}}
    response = await graph.ainvoke({"messages": chat_input.messages}, config=config)
    return response["messages"][-1].content


@app.get("/")
def get():
    return HTMLResponse(html)


@app.websocket("/ws/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str, graph=Depends(get_graph)):
    config = {"configurable": {"thread_id": thread_id}}
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        async for event in graph.astream({"messages": [data]}, config=config, stream_mode="messages"):
            await websocket.send_text(event[0].content)


if __name__ == "__main__":
    import sys
    import asyncio
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    import uvicorn
    uvicorn.run(app)