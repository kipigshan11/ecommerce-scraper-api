import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def scrape_with_playwright(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        content = page.content()
        browser.close()
        return content

def extract_amazon_data(soup):
    title_elem = soup.find(id="productTitle")
    title = title_elem.get_text().strip() if title_elem else "N/A"

    price_elem = soup.find("span", class_="a-price-whole")
    price_fraction = soup.find("span", class_="a-price-fraction")
    
    if price_elem:
        price = price_elem.get_text().strip().replace("\n", "").replace(".", "")
        if price_fraction:
            price += "." + price_fraction.get_text().strip()
    else:
        price = "N/A"

    rating_elem = soup.find("span", class_="a-icon-alt")
    rating = rating_elem.get_text().strip() if rating_elem else "N/A"

    return {"platform": "Amazon", "title": title, "price": price, "rating": rating}

def extract_ebay_data(soup):
    title_elem = soup.find("h1", class_="x-item-title__mainTitle")
    title = title_elem.get_text().strip() if title_elem else "N/A"

    price_elem = soup.find("div", class_="x-price-primary")
    price = price_elem.get_text().strip() if price_elem else "N/A"

    return {"platform": "eBay", "title": title, "price": price, "rating": "N/A"}

def scrape_ecommerce_product(url: str):
    html_content = scrape_with_playwright(url)
    soup = BeautifulSoup(html_content, "html.parser")

    if "amazon" in url.lower():
        return extract_amazon_data(soup)
    elif "ebay" in url.lower():
        return extract_ebay_data(soup)
    else:
        title_elem = soup.find("h1")
        title = title_elem.get_text().strip() if title_elem else "Title not found"
        return {"platform": "Generic E-commerce", "title": title, "price": "Check website", "rating": "N/A"}