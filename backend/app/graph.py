from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from app.llm import llm_model
from app.context_manager import trim_messages
from app.memory import get_checkpointer
from functools import lru_cache


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    state["messages"] = trim_messages(state["messages"], max_tokens=4000)
    system_message = "You are a helpful assistant. You are a pirate. Talk like a pirate."
    response = llm_model.invoke({"system_message": system_message, "messages": state["messages"]})
    return {"messages": [response]}


async def get_graph():
    checkpointer = await get_checkpointer()
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    graph = graph_builder.compile(checkpointer=checkpointer)
    return graph
