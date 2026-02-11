import csv
import re
from typing import Dict, List, Set

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init


EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
SOCIAL_DOMAINS = ("instagram.com", "linkedin.com", "twitter.com", "x.com")


def fetch_page(url: str) -> str:
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.text


def extract_emails(text: str) -> Set[str]:
    return set(match.lower() for match in EMAIL_REGEX.findall(text))


def extract_social_links(soup: BeautifulSoup) -> Set[str]:
    links = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if any(domain in href for domain in SOCIAL_DOMAINS):
            links.add(href)
    return links


def extract_mailto_emails(soup: BeautifulSoup) -> Set[str]:
    emails = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if href.lower().startswith("mailto:"):
            mailto_value = href[7:].split("?", 1)[0]
            for email in re.split(r"[;,]", mailto_value):
                email = email.strip()
                if email:
                    emails.add(email.lower())
    return emails


def save_to_csv(data: Dict[str, List[str]], filename: str = "leads.csv") -> None:
    with open(filename, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["emails", "social_links"])
        writer.writerow(
            [
                "; ".join(data.get("emails", [])),
                "; ".join(data.get("social_links", [])),
            ]
        )


def main() -> None:
    init(autoreset=True)
    print(Fore.CYAN + "Lead Extractor - Simple contact info scraper")

    url = input(Fore.YELLOW + "Enter a URL to scan: ").strip()
    if not url:
        print(Fore.RED + "No URL provided. Exiting.")
        return

    print(Fore.BLUE + "Fetching page content...")
    try:
        html = fetch_page(url)
    except requests.RequestException as exc:
        print(Fore.RED + f"Failed to fetch URL: {exc}")
        return

    print(Fore.BLUE + "Parsing and extracting data...")
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(separator=" ")

    emails = sorted(extract_emails(page_text).union(extract_mailto_emails(soup)))
    social_links = sorted(extract_social_links(soup))

    results = {"emails": emails, "social_links": social_links}
    save_to_csv(results)

    print(Fore.GREEN + "Extraction complete.")
    print(Fore.MAGENTA + f"Emails found: {len(emails)}")
    for email in emails:
        print(Fore.WHITE + f" - {email}")

    print(Fore.MAGENTA + f"Social links found: {len(social_links)}")
    for link in social_links:
        print(Fore.WHITE + f" - {link}")

    print(Fore.GREEN + "Saved to leads.csv")


if __name__ == "__main__":
    main()
