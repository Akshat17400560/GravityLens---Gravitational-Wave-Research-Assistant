import streamlit as st

from rag_chain import rag_chain

st.set_page_config(
    page_title="Gravitational Wave Research Assistant",
    page_icon="🔭",
    layout="wide"
)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🔭 GravityLens")

    st.markdown("""
    ### Tech Stack

    - Gemini 2.5 Flash
    - LangChain
    - Pinecone
    - RAG
    - Streamlit
    """)

    st.markdown("---")

    st.markdown("""
    ### About

    This assistant answers questions about:

    - Gravitational Waves
    - LIGO & Virgo
    - Black Hole Mergers
    - Neutron Star Collisions
    - GW150914
    """)

# Main Header
st.title("🔭 Gravitational Wave Research Assistant")

st.markdown(
    "Explore gravitational-wave astronomy using a Retrieval-Augmented Generation (RAG) system."
)

# Welcome section
if len(st.session_state.messages) == 0:
    st.info("""
Try asking:

• What are gravitational waves?

• Explain GW150914

• How does LIGO detect black hole mergers?

• What is a chirp signal?

• Difference between neutron star and black hole mergers?
""")

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input(
    "Ask a question about gravitational waves..."
)

if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("🔭 Searching the knowledge base..."):

            response = rag_chain.invoke(question)

        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )