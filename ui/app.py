import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agents import coordinator
import tempfile
import json

st.set_page_config(page_title="📚 Agentic RAG Chatbot", layout="wide")
st.title("Agentic RAG Chatbot 🤖📄")
st.markdown("*Powered by Model Context Protocol (MCP) Agent Architecture*")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "source_chunks" not in st.session_state:
    st.session_state.source_chunks = []
if "message_history" not in st.session_state:
    st.session_state.message_history = []
if "expanded_messages" not in st.session_state:
    st.session_state.expanded_messages = set()  # Track which message details are shown

# Sidebar for file upload and settings
with st.sidebar:
    st.header("📁 Document Upload")
    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True,
                                      type=['pdf', 'docx', 'pptx', 'csv', 'txt', 'md'])

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        for file in uploaded_files:
            st.text(f"• {file.name}")

    st.markdown("---")

    # MCP Message Tracing Toggle
    show_mcp_messages = st.checkbox("🔍 Show MCP Message Flow", value=False)

    st.markdown("---")
    st.markdown("### 🏗️ Agent Architecture")
    st.markdown("""
    **Pipeline Flow:**
    1. 📝 **IngestionAgent** → Parses documents
    2. 🗄️ **RetrievalAgent** → Stores & retrieves chunks  
    3. 🤖 **LLMResponseAgent** → Generates answers

    *All communication via MCP messages*
    """)

# Create columns based on MCP message visibility
if show_mcp_messages:
    col1, col2 = st.columns([2, 1])
else:
    col1 = st.container()
    col2 = None

with col1:
    # Display chat history
    st.markdown("### 💬 Conversation")
    for role, content in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(content)

    # Show most recent sources with better formatting
    if st.session_state.source_chunks:
        with st.expander("📎 Source Chunks Used", expanded=False):
            st.markdown("*These are the document segments used to generate the response:*")

            for i, src in enumerate(st.session_state.source_chunks):
                # Clean up the source chunk
                clean_src = src.strip()
                if clean_src:  # Only show non-empty chunks
                    with st.container():
                        st.markdown(f"**Source {i + 1}:**")
                        # Use text area for better formatting of longer chunks
                        if len(clean_src) > 200:
                            st.text_area("", clean_src, height=100, key=f"source_{i}", disabled=True)
                        else:
                            st.markdown(f"> {clean_src}")
                        st.markdown("---")

# MCP Message Flow Panel
if show_mcp_messages and col2 is not None:
    with col2:
        st.markdown("### 🔄 MCP Message Flow")
        if st.session_state.message_history:
            for i, msg in enumerate(st.session_state.message_history):
                with st.container():
                    # Color code by message type
                    if msg["type"] == "DOC_PARSED":
                        st.success(f"**{msg['sender']}** → **{msg['receiver']}**")
                    elif msg["type"] == "RETRIEVAL_RESULT":
                        st.info(f"**{msg['sender']}** → **{msg['receiver']}**")
                    elif msg["type"] == "LLM_RESPONSE":
                        st.warning(f"**{msg['sender']}** → **{msg['receiver']}**")
                    else:
                        st.text(f"**{msg['sender']}** → **{msg['receiver']}**")

                    st.caption(f"Type: `{msg['type']}`")
                    st.caption(f"Trace ID: `{msg['trace_id'][:8]}...`")

                    # Toggle button for details with unique key using index
                    msg_key = f"msg_{i}_{msg['trace_id'][:8]}"
                    is_expanded = msg_key in st.session_state.expanded_messages

                    button_text = "Hide Details" if is_expanded else "Show Details"

                    if st.button(button_text, key=f"toggle_{msg_key}"):
                        if is_expanded:
                            st.session_state.expanded_messages.remove(msg_key)
                        else:
                            st.session_state.expanded_messages.add(msg_key)
                        st.rerun()

                    # Show payload if expanded
                    if is_expanded:
                        with st.expander("📋 Message Details", expanded=True):
                            st.json(msg["payload"])

                    st.markdown("---")
        else:
            st.info("No messages yet. Upload files and ask a question!")

# Chat input - this stays at the bottom
query = st.chat_input("Ask a question about your documents...")

if query:
    if uploaded_files:
        # Add user message to chat
        st.session_state.chat_history.append(("user", query))

        # Show spinner while processing
        with st.spinner("🔄 Processing through agent pipeline..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                file_paths = []
                for file in uploaded_files:
                    path = f"{tmpdir}/{file.name}"
                    with open(path, "wb") as f:
                        f.write(file.read())
                    file_paths.append(path)

                # Run the pipeline
                response = coordinator.run_pipeline(file_paths, query)

                # Add assistant response to chat history
                st.session_state.chat_history.append(("assistant", response["answer"]))

                # Update source chunks and message history
                st.session_state.source_chunks = response["sources"]
                st.session_state.message_history = response.get("message_history", [])

        # Rerun to display the new messages
        st.rerun()
    else:
        st.warning("⚠️ Please upload files first to ask questions about them.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>🏗️ Built with Agentic Architecture • 🤖 Powered by MCP • 📚 Multi-format Document Support</small>
</div>
""", unsafe_allow_html=True)