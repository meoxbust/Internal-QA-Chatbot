import streamlit as st
from model import QASystem

# Set page configuration for a professional, chat-like look
st.set_page_config(
    page_title="Internal Document Q&A",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a polished, professional chat UI
st.markdown("""
    <style>
    /* General styling */
    body {
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background-color: #f5f6f5;
    }
    /* Header styling */
    h1 {
        color: #1e3a8a;
        font-weight: 600;
        margin-bottom: 10px;
    }
    /* Chat message styling */
    .stChatMessage {
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }
    /* User message */
    .stChatMessage.user {
        background-color: #e6f3ff;
        border: 1px solid #bfdbfe;
    }
    /* Assistant message */
    .stChatMessage.assistant {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
    }
    /* Chat input */
    .stChatInput > div > input {
        border: 1px solid #d1d5db;
        border-radius: 4px;
        padding: 8px;
    }
    /* Expander for context */
    .stExpander {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 4px;
    }
    /* Sidebar */
    .stSidebar {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation and information
st.sidebar.title("Internal Document Q&A")
st.sidebar.markdown("""This system allows employees to ask questions based on internal company documents (e.g., HR policies, product specifications). 
The system retrieves relevant information and provides accurate, concise answers.""")
st.sidebar.markdown("---")
st.sidebar.markdown("**How to Use**")
st.sidebar.markdown("""
1. Type your question in the chat input at the bottom.
2. Press Enter to receive an answer.
3. Click the expander below the answer to view the supporting document context.
4. Scroll up to review the conversation history.
""")

# Main title
st.title("Internal Document Q&A System")

# Initialize session state

# Place absolute path to your documents folder here
docs_path = r"E:\Interview\Artiv\documents"
if "qa_system" not in st.session_state:
    st.session_state.qa_system = QASystem(docs_path=docs_path)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "context" in message:
            with st.expander("View Supporting Context"):
                st.markdown("The answer is based on the following document excerpt:")
                st.code(message["context"], language="markdown")

# Accept user input via chat input
if prompt := st.chat_input("Ask a question about company documents..."):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            # Get answer and context from QASystem
            answer = st.session_state.qa_system.ask(prompt)
            context = st.session_state.qa_system.retriever.invoke(prompt)
            context_text = "\n\n---\n\n".join(doc.page_content for doc in context)
            
            # Display answer
            st.markdown(answer)
            
            # Display context in an expander
            with st.expander("View Supporting Context"):
                st.markdown("The answer is based on the following document excerpt:")
                st.code(context_text, language="markdown")
        
        # Add assistant message to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "context": context_text
        })