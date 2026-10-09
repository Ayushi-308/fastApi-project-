from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant. "
        "Answer the user's questions clearly and simply."
    ),
    (
        "human",
        "{question}"
    )
])