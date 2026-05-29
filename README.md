# 🔍 AI Research Agent

An autonomous AI research agent that takes a question, searches the web, reads articles, and generates a structured report with citations — all automatically.

Built with LangGraph, Tavily, and Groq LLama 3 (free).

## What it does

You type a question like "What are the latest AI trends in 2025?" and the agent automatically:
- Plans 3 search queries
- Searches the web using Tavily
- Reads and scores each source for credibility
- Synthesizes findings with citations
- Writes a structured report and saves it

## How to run

1. Clone the repo
git clone https://github.com/yeshwanthkommoji-pixel/ai-research-agent.git

2. Install dependencies
pip install -r requirements.txt

3. Add your API keys - create a .env file
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here

4. Run from terminal
python main.py --query "Your question here"

5. Run the web UI
python -m streamlit run app.py

## Tech Stack
- LangGraph — agentic workflow
- Tavily — real time web search
- Groq LLama 3 — free AI reasoning
- BeautifulSoup4 — article reader
- Streamlit — web UI

## License
MIT
