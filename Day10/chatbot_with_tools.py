from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver


from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import ToolNode, tools_condition
import sqlite3
import requests


load_dotenv()

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model="openrouter/free"
)
#state
class ChatState(TypedDict):
    messages: Annotated[list[str], add_messages]



#tools


search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}



tools=[search_tool,calculator]

llm_with_tools=model.bind_tools(tools)


#nodes
def chat(state: ChatState):

    """LLM node that may answer or request a tool call."""
    messages = state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


tool_node=ToolNode(tools)



#checkpointer


con=sqlite3.connect(database='chatbot.db',check_same_thread=False  )
checkpointer=SqliteSaver(conn=con)

#graph
graph = StateGraph(ChatState)

graph.add_node("chat", chat)
graph.add_node('tools',tool_node)



graph.add_edge(START, "chat")
graph.add_conditional_edges('chat',tools_condition)
graph.add_edge('tools', 'chat')

chatbot = graph.compile(checkpointer=checkpointer)

thread_id=4

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