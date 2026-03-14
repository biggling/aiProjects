"""Product CRUD endpoints — reads/writes config/products.yaml."""

import asyncio
from pathlib import Path

import yaml
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl

from api.deps import verify_api_key

router = APIRouter(prefix="/api/products", tags=["products"], dependencies=[Depends(verify_api_key)])

PRODUCTS_PATH = Path("config/products.yaml")


class ProductModel(BaseModel):
    id: str
    name: str
    tiktok_shop_url: str = ""
    commission_rate: float = 0.0
    affiliate_link: str = ""
    utm_source: str = "tiktok"
    utm_campaign: str = ""
    approved: bool = False


class ProductCreate(BaseModel):
    name: str
    tiktok_shop_url: str = ""
    commission_rate: float = 0.0
    affiliate_link: str = ""
    utm_source: str = "tiktok"
    utm_campaign: str = ""
    approved: bool = False


class ProductUpdate(BaseModel):
    name: str | None = None
    tiktok_shop_url: str | None = None
    commission_rate: float | None = None
    affiliate_link: str | None = None
    utm_source: str | None = None
    utm_campaign: str | None = None
    approved: bool | None = None


def _load_products() -> list[dict]:
    data = yaml.safe_load(PRODUCTS_PATH.read_text())
    return data.get("products", [])


def _save_products(products: list[dict]):
    PRODUCTS_PATH.write_text(yaml.dump({"products": products}, allow_unicode=True, default_flow_style=False))


@router.get("", response_model=list[ProductModel])
async def list_products():
    products = await asyncio.to_thread(_load_products)
    return products


@router.post("", response_model=ProductModel)
async def create_product(body: ProductCreate):
    products = await asyncio.to_thread(_load_products)
    new_id = f"prod_{len(products) + 1:03d}"
    product = {"id": new_id, **body.model_dump()}
    products.append(product)
    await asyncio.to_thread(_save_products, products)
    return product


@router.put("/{product_id}", response_model=ProductModel)
async def update_product(product_id: str, body: ProductUpdate):
    products = await asyncio.to_thread(_load_products)
    for i, p in enumerate(products):
        if p["id"] == product_id:
            updates = body.model_dump(exclude_none=True)
            products[i].update(updates)
            await asyncio.to_thread(_save_products, products)
            return products[i]
    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/{product_id}")
async def delete_product(product_id: str):
    products = await asyncio.to_thread(_load_products)
    products = [p for p in products if p["id"] != product_id]
    await asyncio.to_thread(_save_products, products)
    return {"status": "deleted", "id": product_id}
