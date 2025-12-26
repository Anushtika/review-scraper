import requests
from bs4 import BeautifulSoup
import json
import argparse
from datetime import datetime
import sys


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ReviewScraper/1.0)"
}


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)


def within_range(date, start, end):
    return start <= date <= end


# -------------------- G2 SCRAPER --------------------
def scrape_g2(company, start_date, end_date):
    reviews = []
    page = 1

    while True:
        url = f"https://www.g2.com/products/{company.lower().replace(' ', '-')}/reviews?page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        review_blocks = soup.select(".paper.paper--white.paper--box")

        if not review_blocks:
            break

        for block in review_blocks:
            try:
                title = block.select_one("h3").text.strip()
                description = block.select_one(".formatted-text").text.strip()
                date_text = block.select_one("time")["datetime"][:10]
                review_date = datetime.strptime(date_text, "%Y-%m-%d")

                if review_date < start_date:
                    return reviews

                if within_range(review_date, start_date, end_date):
                    reviews.append({
                        "title": title,
                        "review": description,
                        "date": date_text,
                        "source": "G2"
                    })
            except Exception:
                continue

        page += 1

    return reviews


# -------------------- CAPTERRA SCRAPER --------------------
def scrape_capterra(company, start_date, end_date):
    reviews = []
    page = 1

    while True:
        url = f"https://www.capterra.com/p/{company.lower().replace(' ', '-')}/reviews/?page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        review_blocks = soup.select(".review")

        if not review_blocks:
            break

        for block in review_blocks:
            try:
                title = block.select_one(".review-title").text.strip()
                description = block.select_one(".review-comment").text.strip()
                date_text = block.select_one("time").text.strip()
                review_date = datetime.strptime(date_text, "%B %d, %Y")

                if review_date < start_date:
                    return reviews

                if within_range(review_date, start_date, end_date):
                    reviews.append({
                        "title": title,
                        "review": description,
                        "date": review_date.strftime("%Y-%m-%d"),
                        "source": "Capterra"
                    })
            except Exception:
                continue

        page += 1

    return reviews


# -------------------- TRUST RADIUS (BONUS) --------------------
def scrape_trustradius(company, start_date, end_date):
    reviews = []
    page = 1

    while True:
        url = f"https://www.trustradius.com/products/{company.lower().replace(' ', '-')}/reviews?page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        review_blocks = soup.select(".review-content")

        if not review_blocks:
            break

        for block in review_blocks:
            try:
                title = block.select_one("h3").text.strip()
                description = block.select_one(".review-body").text.strip()
                date_text = block.select_one("time")["datetime"][:10]
                review_date = datetime.strptime(date_text, "%Y-%m-%d")

                if review_date < start_date:
                    return reviews

                if within_range(review_date, start_date, end_date):
                    reviews.append({
                        "title": title,
                        "review": description,
                        "date": date_text,
                        "source": "TrustRadius"
                    })
            except Exception:
                continue

        page += 1

    return reviews


# -------------------- MAIN --------------------
def main():
    parser = argparse.ArgumentParser(description="SaaS Review Scraper")
    parser.add_argument("--company", required=True)
    parser.add_argument("--source", required=True, choices=["g2", "capterra", "trustradius"])
    parser.add_argument("--start_date", required=True)
    parser.add_argument("--end_date", required=True)
    parser.add_argument("--output", default="reviews.json")

    args = parser.parse_args()

    start_date = parse_date(args.start_date)
    end_date = parse_date(args.end_date)

    if start_date > end_date:
        print("Start date must be before end date.")
        sys.exit(1)

    if args.source == "g2":
        data = scrape_g2(args.company, start_date, end_date)
    elif args.source == "capterra":
        data = scrape_capterra(args.company, start_date, end_date)
    else:
        data = scrape_trustradius(args.company, start_date, end_date)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Scraped {len(data)} reviews → {args.output}")


if __name__ == "__main__":
    main()
