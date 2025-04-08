from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "{system_message}"),
        MessagesPlaceholder("messages")
    ]
)
llm_model = prompt_template | llm
