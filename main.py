#!/usr/bin/env python3
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

from agent.graph import research_agent
from utils.report import export_pdf


def main():
    parser = argparse.ArgumentParser(
        description="AI Research Agent — powered by LangGraph + Tavily + Claude"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        required=True,
        help="The research question to investigate",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Also export the report as a PDF",
    )
    args = parser.parse_args()

    print(f"\n🚀 Starting AI Research Agent")
    print(f"📌 Query: {args.query}")
    print("=" * 60)

    result = research_agent.invoke({"query": args.query})

    print("\n" + "=" * 60)
    print(result["report"])

    if args.pdf:
        pdf_path = f"outputs/report_{args.query[:30].replace(' ', '_')}.pdf"
        export_pdf(result["report"], pdf_path)


if __name__ == "__main__":
    main()