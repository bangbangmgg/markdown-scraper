import sys
import argparse
import urllib.request
import json
from html.parser import HTMLParser

class SimpleHTMLFilter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.text.append(text)

def fetch_url(url):
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            parser = SimpleHTMLFilter()
            parser.feed(html)
            return "\n".join(parser.text)
    except Exception as e:
        return f"Error fetching {url}: {e}"

def main():
    parser = argparse.ArgumentParser(description="Fast CLI Web to Text Scraper for LLMs & RAG")
    parser.add_argument("url", help="Target URL to scrape")
    parser.add_argument("-o", "--output", help="Output file path", default=None)
    args = parser.parse_args()

    print(f"Scraping {args.url}...")
    content = fetch_url(args.url)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to {args.output}")
    else:
            print("\n--- Extracted Content ---")
            print(content[:2000])
            print("\n... [Truncated for preview] ...")

if __name__ == "__main__":
    main()
