import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com/products/product-catalog/"


def classify_test_type(name):
    lower_name = name.lower()

    if any(word in lower_name for word in [
        "java", "python", "sql", "javascript", ".net",
        "cloud", "api", "developer", "coding", "technical"
    ]):
        return "Technical Skill"

    elif any(word in lower_name for word in [
        "personality", "opq", "motivation"
    ]):
        return "Behavioral"

    elif any(word in lower_name for word in [
        "cognitive", "verify", "reasoning", "ability"
    ]):
        return "Cognitive"

    elif any(word in lower_name for word in [
        "situational", "judgement", "sjt"
    ]):
        return "Behavioral"

    return "General"


def scrape_shl_catalog():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    assessments = []
    seen = set()

    for start in range(0, 400, 12):
        url = f"{BASE_URL}?start={start}&type=1"
        print(f"Scraping: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print("Skipping page...")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            for link in links:
                href = link["href"]
                name = link.get_text(strip=True)

                if "/products/product-catalog/view/" in href and name:
                    full_url = href if href.startswith("http") else f"https://www.shl.com{href}"

                    if full_url not in seen:
                        seen.add(full_url)

                        assessments.append({
                            "name": name,
                            "url": full_url,
                            "test_type": classify_test_type(name)
                        })

            time.sleep(1)

        except Exception as e:
            print("Error:", e)

    with open("data/catalog.json", "w", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2)

    print(f"Saved {len(assessments)} SHL assessments")


if __name__ == "__main__":
    scrape_shl_catalog()