from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage



import  sqlite3 

from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model="openrouter/free"
)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }

thread_id = 2

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

con=sqlite3.connect(database='chatbot.db',check_same_thread=False)


checkpointer = SqliteSaver(conn=con)

chatbot = graph.compile(
    checkpointer=checkpointer
)

while True:
    user_message = input("Type here: ")
    print(f"\nUser: {user_message}")

    if user_message.strip().lower() in ["exit", "bye", "quit"]:
        break

    config = {"configurable": {"thread_id": thread_id}}

    print("AI: ", end="")

    for message_chunk, metadata in chatbot.stream(
        {"messages": [HumanMessage(content=user_message)]},
        config=config,
        stream_mode="messages"
    ):
        if message_chunk.content:
            print(message_chunk.content, end="", flush=True)

    print("\n")

state=chatbot.get_state(config)
print(state)