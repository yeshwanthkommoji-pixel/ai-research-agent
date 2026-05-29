import requests
from bs4 import BeautifulSoup
from typing import Optional

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
MAX_CHARS = 3000


def extract_article_content(url: str) -> Optional[str]:
    try:
        response = requests.get(url, headers=HEADERS, timeout=8)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        article = soup.find("article") or soup.find("main") or soup.find("body")
        if not article:
            return None

        text = article.get_text(separator=" ", strip=True)

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = " ".join(lines)

        return clean_text[:MAX_CHARS]

    except Exception:
        return None