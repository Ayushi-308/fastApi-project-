from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant. "
        "Answer the user's questions clearly and simply."
    ),

    MessagesPlaceholder(variable_name="chat_history"),

    (
        "human",
        "{question}"
    )
])