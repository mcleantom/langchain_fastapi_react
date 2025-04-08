from tiktoken import encoding_for_model
from langgraph.graph.message import BaseMessage


def count_tokens(messages: list[BaseMessage]) -> int:
    encoding = encoding_for_model("gpt-4o-mini")
    num_tokens = 0
    for message in messages:
        num_tokens += len(encoding.encode(message.content))
        num_tokens += 4
    return num_tokens


def trim_messages(messages: list[BaseMessage], max_tokens: int = 4000) -> list[BaseMessage]:
    if not messages:
        return messages
    system_message = None
    chat_messages = messages.copy()

    if messages[0].type == "system":
        system_message = chat_messages.pop(0)

    current_tokens = count_tokens(chat_messages)

    while current_tokens > max_tokens and len(chat_messages) > 1:
        chat_messages.pop(0)
        current_tokens = count_tokens(chat_messages)

    if system_message:
        chat_messages.insert(0, system_message)

    for message in chat_messages:
        print(message)

    return chat_messages

