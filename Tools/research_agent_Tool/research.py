from tavily import TavilyClient
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests


import os

load_dotenv()


Client = TavilyClient(os.getenv("TAVILY_API_KEY"))


def search(query):
    search = Client.search(query, timeout=10)

    search_content = []

    for r in search["results"]:
        url = r["url"]
        search_content.append(url)
    return search_content


def extract_content(url):
    url_result = requests.get(url=url)
    supe = BeautifulSoup(url_result.text, "html.parser")
    for tags in supe(
        [
            "script",
            "style",
            "nav",
            "header",
            "footer",
            "aside",
            "noscript",
            "svg",
            "iframe",
            "form",
            "button",
        ]
    ):
        tags.decompose()
    text = supe.get_text(separator=" ", strip=True)
    print("text", text)
    return text


def research(query):
    search_result = search(query)

    all_content = []

    for url in search_result:
        extract_content_result = extract_content(url)
        all_content.append(extract_content_result)
    return "\n\n ".join(all_content)
