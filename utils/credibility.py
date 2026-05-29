from urllib.parse import urlparse

HIGH_CREDIBILITY_DOMAINS = {
    "reuters.com", "bbc.com", "bbc.co.uk", "nytimes.com", "theguardian.com",
    "nature.com", "science.org", "pubmed.ncbi.nlm.nih.gov", "arxiv.org",
    "mit.edu", "stanford.edu", "harvard.edu", "who.int", "gov", "ac.uk",
    "economist.com", "ft.com", "wsj.com", "bloomberg.com", "apnews.com",
    "techcrunch.com", "wired.com", "arstechnica.com", "ieee.org",
}

LOW_CREDIBILITY_DOMAINS = {
    "reddit.com", "quora.com", "yahoo.answers.com", "pinterest.com",
    "buzzfeed.com", "dailymail.co.uk",
}


def score_source(url: str, content: str | None) -> float:
    score = 0.5

    try:
        domain = urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return 0.0

    if any(hd in domain for hd in HIGH_CREDIBILITY_DOMAINS):
        score += 0.35
    elif any(ld in domain for ld in LOW_CREDIBILITY_DOMAINS):
        score -= 0.3

    if content:
        word_count = len(content.split())
        if word_count > 300:
            score += 0.1
        if word_count < 50:
            score -= 0.2

    if url.startswith("https://"):
        score += 0.05

    return max(0.0, min(1.0, score))