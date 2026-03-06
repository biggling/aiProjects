"""Etsy, Printify, and Redbubble API clients."""
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from config import (
    ETSY_API_KEY, ETSY_ACCESS_TOKEN, ETSY_SHOP_ID, ETSY_BASE_URL,
    PRINTIFY_API_KEY, PRINTIFY_SHOP_ID, PRINTIFY_BASE_URL,
    get_logger,
)

logger = get_logger("platform_api")


class EtsyClient:
    def __init__(self):
        self.base = ETSY_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {ETSY_ACCESS_TOKEN}",
            "x-api-key": ETSY_API_KEY,
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def get_listings(self, limit: int = 25, offset: int = 0) -> list:
        url = f"{self.base}/application/shops/{ETSY_SHOP_ID}/listings/active"
        r = requests.get(url, headers=self.headers,
                         params={"limit": limit, "offset": offset}, timeout=15)
        r.raise_for_status()
        return r.json().get("results", [])

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def get_receipts(self, limit: int = 25, offset: int = 0) -> list:
        url = f"{self.base}/application/shops/{ETSY_SHOP_ID}/receipts"
        r = requests.get(url, headers=self.headers,
                         params={"limit": limit, "offset": offset}, timeout=15)
        r.raise_for_status()
        return r.json().get("results", [])

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def update_listing(self, listing_id: str, data: dict) -> dict:
        url = f"{self.base}/application/shops/{ETSY_SHOP_ID}/listings/{listing_id}"
        r = requests.patch(url, headers=self.headers, json=data, timeout=15)
        r.raise_for_status()
        return r.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def search_listings(self, keyword: str, limit: int = 20) -> list:
        url = f"{self.base}/application/listings/active"
        r = requests.get(url, headers=self.headers,
                         params={"keywords": keyword, "limit": limit}, timeout=15)
        r.raise_for_status()
        return r.json().get("results", [])


class PrintifyClient:
    def __init__(self):
        self.base = PRINTIFY_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {PRINTIFY_API_KEY}",
            "Content-Type": "application/json",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def get_products(self) -> list:
        url = f"{self.base}/shops/{PRINTIFY_SHOP_ID}/products.json"
        r = requests.get(url, headers=self.headers, timeout=15)
        r.raise_for_status()
        return r.json().get("data", [])

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def upload_image(self, filename: str, contents_b64: str) -> dict:
        url = f"{self.base}/uploads/images.json"
        r = requests.post(url, headers=self.headers,
                          json={"file_name": filename, "contents": contents_b64}, timeout=60)
        r.raise_for_status()
        return r.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def create_product(self, product_data: dict) -> dict:
        url = f"{self.base}/shops/{PRINTIFY_SHOP_ID}/products.json"
        r = requests.post(url, headers=self.headers, json=product_data, timeout=30)
        r.raise_for_status()
        return r.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def publish_product(self, product_id: str, publish_data: dict) -> dict:
        url = f"{self.base}/shops/{PRINTIFY_SHOP_ID}/products/{product_id}/publish.json"
        r = requests.post(url, headers=self.headers, json=publish_data, timeout=30)
        r.raise_for_status()
        return r.json()


class PinterestClient:
    def __init__(self):
        from config import PINTEREST_ACCESS_TOKEN, PINTEREST_BASE_URL
        self.base = PINTEREST_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def get_boards(self) -> list:
        r = requests.get(f"{self.base}/boards", headers=self.headers, timeout=15)
        r.raise_for_status()
        return r.json().get("items", [])

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def create_board(self, name: str, description: str = "") -> dict:
        r = requests.post(f"{self.base}/boards", headers=self.headers,
                          json={"name": name, "description": description}, timeout=15)
        r.raise_for_status()
        return r.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def create_pin(self, board_id: str, media_url: str, title: str,
                   description: str, link: str) -> dict:
        payload = {
            "board_id": board_id,
            "media_source": {"source_type": "image_url", "url": media_url},
            "title": title,
            "description": description,
            "link": link,
        }
        r = requests.post(f"{self.base}/pins", headers=self.headers,
                          json=payload, timeout=15)
        r.raise_for_status()
        return r.json()
