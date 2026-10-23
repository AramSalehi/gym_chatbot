"""Streamlit chat interface for Ironharbor Fitness.

Run it locally:    python -m streamlit run app.py
"""

import sys

if sys.version_info < (3, 10):
    sys.exit(
        "\nThis project needs Python 3.10 or newer — you're on "
        f"{sys.version.split()[0]}.\n"
        "Create a 3.10+ virtual environment first; see SETUP.md in the project root.\n"
    )

import os

import streamlit as st

# ---------------------------------------------------------------------------
# Page setup and API key
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Ironharbor Fitness Assistant", page_icon="💪")

# Locally, the key comes from your environment (see README step 2).
# On Streamlit Community Cloud, it comes from the app's Secrets panel.
try:
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    pass  # no secrets file locally — that's fine, we check the env var next

if not os.environ.get("OPENAI_API_KEY"):
    st.error(
        "No API key found. Set the OPENAI_API_KEY environment variable "
        "(or add it to Secrets if you're on Streamlit Cloud), then refresh."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Ensure the document database exists
# ---------------------------------------------------------------------------

from ingest import DB_DIR  # the real database location (/tmp/... on Cloud)

@st.cache_resource(show_spinner="First run: reading your documents… (about a minute)")
def ensure_database():
    if not os.path.exists(DB_DIR):
        from ingest import build_database
        build_database()
    return True

ensure_database()

from chatbot import build_agent, safe_answer  # imported after the key is set


@st.cache_resource  # build the agent once, not on every click
def get_agent():
    return build_agent()


agent = get_agent()

# ---------------------------------------------------------------------------
# Sidebar with gym information and a clear-chat button
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("💪 About")
    st.write(
        "I'm the assistant for Ironharbor Fitness. Ask me about memberships, "
        "classes, facilities, training, and gym policies — answers show their sources."
    )
    if st.button("🧹 Clear chat"):
        st.session_state.history = []
        st.rerun()

# ---------------------------------------------------------------------------
# Chat interface
# ---------------------------------------------------------------------------

st.title("💪 Ironharbor Fitness Assistant")
st.caption(
    "Ask me about Ironharbor Fitness — memberships, classes, facilities, "
    "training, and policies. Every answer shows its sources."
)

if "history" not in st.session_state:
    st.session_state.history = []


def show_citations(citations: list[dict]):
    """Render each citation as a clickable, expandable source.
    De-duplicates so the same passage never shows up twice."""
    seen = set()
    for c in citations:
        key = (c["source"], c["quote"])
        if key in seen:
            continue
        seen.add(key)
        with st.expander(f"📄 Source: {c['source']}"):
            # Prefix every line with "> " so multi-paragraph quotes stay fully quoted
            quote = c["quote"].replace("\n", "\n> ")
            st.markdown(f"> {quote}")


# Replay the conversation so far
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        show_citations(msg.get("citations", []))

# Handle a new question
question = st.chat_input("Ask a question about Ironharbor Fitness…")

if question:
    st.session_state.history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the documents…"):
            # Send the whole conversation so the bot remembers context
            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.history
            ]
            # safe_answer() never returns None, so the UI can't crash here
            response = safe_answer(agent.invoke({"messages": messages}))

        st.write(response.answer)
        citations = [{"source": c.source, "quote": c.quote} for c in response.citations]
        show_citations(citations)

    st.session_state.history.append(
        {"role": "assistant", "content": response.answer, "citations": citations}
    )
