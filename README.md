# 🔍 AI Research Agent

An autonomous AI research agent that takes a question, searches the web, reads articles, and generates a structured report with citations — all automatically.

Built with LangGraph, Tavily, and Groq LLama 3.

## Live Demo

https://ai-research-agent-app.streamlit.app

## What it does

You type a question like "What are the latest AI trends in 2025?" and the agent automatically:

- Plans 3 search queries
- Searches the web using Tavily
- Reads and scores each source for credibility
- Synthesizes findings with citations
- Writes a structured report

## Tech Stack

- LangGraph — agentic workflow
- Tavily — real time web search
- Groq LLama 3 — AI reasoning
- BeautifulSoup4 — article reader
- Streamlit — web UI
