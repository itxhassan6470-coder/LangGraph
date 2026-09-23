import streamlit as st

from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage


st.title("LangGraph Chatbot")


# IMPORTANT:
# Same thread_id = same conversation
CONFIG = {
    "configurable": {
        "thread_id": "hassan_chat_1"
    }
}


# Get previous conversation from LangGraph
state = chatbot.get_state(CONFIG)


# Display previous messages
for message in state.values.get("messages", []):

    if isinstance(message, HumanMessage):
        role = "user"
    else:
        role = "assistant"

    with st.chat_message(role):
        st.write(message.content)


# User input
user_input = st.chat_input("Type your message...")


if user_input:

    # Display user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # Send to LangGraph
    response = chatbot.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        config=CONFIG
    )

    # Get latest AI response
    ai_message = response["messages"][-1]

    # Display AI response
    with st.chat_message("assistant"):
        st.write(ai_message.content)