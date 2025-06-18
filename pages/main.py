import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory 
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import trim_messages
from operator import itemgetter
from langchain_community.chat_models import ChatOllama

# 1. Title
st.title("💬 Ask More About Your Recommended Cards")

# 2. Check if card recommendations exist
if "recommended_cards" not in st.session_state:
    st.warning("🔙 Please start from the home page.")
    st.stop()

recommended_cards = st.session_state.recommended_cards

# 3. Format card context
card_context = "\n\n".join(
    f"Card Name: {card['Card Name']}\nUSP: {card['USP']}\nPros: {card['Pros']}\nCons: {card['Cons']}"
    for card in recommended_cards
)

# Store card context in session for use in prompt
st.session_state.card_context = card_context

# 4. Set up chat memory store
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 5. Define prompt with dynamic card context
system_prompt = (
    "You are AdityaChatBot, an AI-powered credit card assistant developed by Aditya Kalsi. "
    "Here is a summary of the recommended cards:\n\n"
    + st.session_state.card_context +
    "\n\nNow, answer the user's follow-up questions based only on this information. "
    "Be helpful, friendly, and accurate."
)

# 6. Prompt structure
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages")
    ]
)

# 7. Chat response generator
def generate_response(question, messages):
    llm = ChatOllama(model="mistral", temperature=0.7)
    output_parser = StrOutputParser()

    trimmer = trim_messages(
        max_tokens=128000,
        strategy="last",
        token_counter=llm,
        include_system=True,
        allow_partial=False,
        start_on="human"
    )

    chain = (
        RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
        | prompt
        | llm
        | output_parser
    )

    with_message_history = RunnableWithMessageHistory(
        chain, get_session_history, input_messages_key="messages"
    )

    config = {"configurable": {"session_id": "chat_session_1"}}

    response = with_message_history.invoke(
        {
            "messages": messages + [HumanMessage(content=question)],
        },
        config=config
    )

    return response

# 8. Chat UI
st.markdown("### 💡 Ask anything about the recommended cards")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input("Ask a question:")
if st.button("Send") and question:
    response = generate_response(
        question=question,
        messages=st.session_state.chat_history
    )

    st.session_state.chat_history.append(HumanMessage(content=question))
    st.session_state.chat_history.append(AIMessage(content=response))

# 9. Display chat history
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)
