import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from agent.graph import research_agent

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 AI Research Agent")
st.caption("Powered by LangGraph · Tavily · Claude")

with st.sidebar:
    st.header("⚙️ Settings")
    max_iter = st.slider("Max search iterations", 1, 5, 3)
    export_pdf = st.checkbox("Export as PDF", value=False)
    st.divider()
    st.markdown("**How it works:**")
    st.markdown("""
1. 📋 Plans search queries
2. 🌐 Searches the web (Tavily)
3. 📖 Reads & scores sources
4. 🧠 Synthesizes with Claude
5. 📄 Writes structured report
    """)

query = st.text_input(
    "Enter your research question:",
    placeholder="e.g. What is the current state of AI regulation in the EU?",
)

if st.button("🚀 Start Research", type="primary", disabled=not query):
    os.environ["MAX_SEARCH_ITERATIONS"] = str(max_iter)

    with st.status("Researching...", expanded=True) as status:
        st.write("📋 Planning search queries...")

        result = None
        for step in research_agent.stream({"query": query}):
            node_name = list(step.keys())[0]
            node_icons = {
                "plan": "📋 Planning searches...",
                "search": "🌐 Searching the web...",
                "evaluate": "📊 Evaluating sources...",
                "synthesize": "🧠 Synthesizing findings...",
                "report": "📄 Writing report...",
            }
            st.write(node_icons.get(node_name, f"⚙️ {node_name}..."))
            result = step[node_name]

        status.update(label="✅ Research complete!", state="complete")

    if result and result.get("report"):
        st.divider()

        col1, col2, col3 = st.columns(3)
        col1.metric("Sources Found", len(result.get("sources", [])))
        col2.metric("Search Iterations", result.get("iterations", 0))
        col3.metric("Queries Run", len(result.get("search_queries", [])))

        st.divider()
        st.markdown(result["report"])

        st.download_button(
            label="⬇️ Download Report (Markdown)",
            data=result["report"],
            file_name=f"research_{query[:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )

        if export_pdf:
            from utils.report import export_pdf as make_pdf
            pdf_path = f"outputs/report_{query[:30].replace(' ', '_')}.pdf"
            make_pdf(result["report"], pdf_path)
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Report (PDF)",
                        data=f.read(),
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                    )