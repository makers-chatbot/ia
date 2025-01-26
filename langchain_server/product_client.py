import httpx
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Product(BaseModel):
    id: str
    name: str
    brand: str
    model: Optional[str] = None
    description: str
    price: float
    stock: int
    warrantyPeriod: int
    releaseDate: int
    specifications: Optional[Dict] = None
    images: Optional[Dict] = {}
    category: str
    # Optional fields based on category
    processor: Optional[str] = None
    ram: Optional[str] = None
    storageType: Optional[str] = None
    storageCapacity: Optional[str] = None
    graphicsCard: Optional[str] = None
    operatingSystem: Optional[str] = None
    printingTechnology: Optional[str] = None
    connectivityOptions: Optional[List[str]] = None

    class Config:
        extra = "ignore"
        validate_assignment = True
        arbitrary_types_allowed = True


class ProductClient:
    def __init__(self, base_url: str = "http://localhost:8081/api"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=10.0)
        logger.info(f"ProductClient initialized with base URL: {base_url}")

    async def get_products(self) -> List[Product]:
        """Fetch all products from the backend API"""
        logger.info("Attempting to fetch products from backend")
        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"Making GET request to {self.base_url}/products")
                response = await client.get(f"{self.base_url}/products")
                logger.info(f"Response status code: {response.status_code}")

                response.raise_for_status()
                products_data = response.json()
                logger.info(f"Successfully fetched {len(products_data)} products")
                logger.debug(f"Raw products data: {products_data}")

                products = [Product(**product) for product in products_data]
                logger.info("Successfully parsed all products")
                return products

        except httpx.RequestError as e:
            logger.error(f"Network error while fetching products: {str(e)}")
            return []
        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error while fetching products: {e.response.status_code} - {e.response.text}"
            )
            return []
        except Exception as e:
            logger.error(f"Unexpected error while fetching products: {str(e)}")
            if hasattr(e, "__traceback__"):
                logger.error(f"Traceback: ", exc_info=True)
            return []

    async def get_product(self, product_id: str) -> Optional[Product]:
        """Fetch a specific product by ID"""
        logger.info(f"Attempting to fetch product with ID: {product_id}")
        try:
            async with httpx.AsyncClient() as client:
                logger.info(
                    f"Making GET request to {self.base_url}/products/{product_id}"
                )
                response = await client.get(f"{self.base_url}/products/{product_id}")
                logger.info(f"Response status code: {response.status_code}")

                response.raise_for_status()
                product_data = response.json()
                logger.info("Successfully fetched product data")
                logger.debug(f"Raw product data: {product_data}")

                product = Product(**product_data)
                logger.info("Successfully parsed product")
                return product

        except httpx.RequestError as e:
            logger.error(f"Network error while fetching product {product_id}: {str(e)}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error while fetching product {product_id}: {e.response.status_code} - {e.response.text}"
            )
            return None
        except Exception as e:
            logger.error(
                f"Unexpected error while fetching product {product_id}: {str(e)}"
            )
            if hasattr(e, "__traceback__"):
                logger.error(f"Traceback: ", exc_info=True)
            return None
