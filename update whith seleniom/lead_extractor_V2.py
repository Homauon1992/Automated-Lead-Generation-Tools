import csv
import re
import time
from typing import Dict, List, Optional, Set

from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
SOCIAL_DOMAINS = ("instagram.com", "linkedin.com", "twitter.com", "x.com")


def build_headless_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def fetch_page(url: str, driver: webdriver.Chrome) -> str:
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    return driver.page_source


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


def extract_emails_from_hrefs(soup: BeautifulSoup) -> Set[str]:
    hrefs = (anchor["href"].strip() for anchor in soup.find_all("a", href=True))
    return extract_emails(" ".join(hrefs))


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
    driver: Optional[webdriver.Chrome] = None
    try:
        driver = build_headless_driver()
        html = fetch_page(url, driver)
    except WebDriverException as exc:
        print(Fore.RED + f"Failed to fetch URL: {exc}")
        return
    finally:
        if driver is not None:
            driver.quit()

    print(Fore.BLUE + "Parsing and extracting data...")
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(separator=" ")

    emails = sorted(
        extract_emails(page_text)
        .union(extract_mailto_emails(soup))
        .union(extract_emails_from_hrefs(soup))
    )
    if not emails:
        print(Fore.YELLOW + "Checking for obfuscated data...")
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
