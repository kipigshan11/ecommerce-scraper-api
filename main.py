from fastapi import FastAPI, HTTPException, Query
from scrapers import scrape_ecommerce_product

app = FastAPI(
    title="Universal E-commerce Product Scraper API",
    description="Extract product details from Amazon, eBay, and other platforms",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Universal E-commerce Scraper API",
        "docs_url": "/docs"
    }

@app.get("/api/v1/scrape")
def scrape_product(url: str = Query(..., description="Target Product URL")):
    if not url.startswith("http://") and not url.startswith("https://"):
        raise HTTPException(status_code=400, detail="Invalid URL format. Include http:// or https://")
    
    try:
        data = scrape_ecommerce_product(url)
        return {
            "status": "success",
            "url": url,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")