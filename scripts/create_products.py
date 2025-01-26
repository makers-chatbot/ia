import httpx
import asyncio
from datetime import datetime, timedelta
import json

# API Configuration
API_BASE_URL = "http://localhost:8081/api"
AUTH_CREDENTIALS = {"username": "admin", "password": "admin"}


class ProductAPI:
    def __init__(self):
        self.token = None
        self.headers = {}

    async def login(self, client: httpx.AsyncClient) -> bool:
        """Authenticate and get JWT token"""
        try:
            print(
                f"Attempting to log in with credentials: {AUTH_CREDENTIALS['username']}"
            )
            response = await client.post(
                f"{API_BASE_URL}/auth/login", json=AUTH_CREDENTIALS
            )
            response.raise_for_status()
            data = response.json()
            self.token = data.get("token")
            if self.token:
                self.headers = {"Authorization": f"Bearer {self.token}"}
                print("✅ Successfully authenticated")
                return True
            print("❌ No token received in response")
            return False
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            return False

    async def create_product(self, client: httpx.AsyncClient, product: dict) -> bool:
        """Create a single product"""
        if not self.token:
            print("❌ Not authenticated. Please login first.")
            return False

        try:
            response = await client.post(
                f"{API_BASE_URL}/products", json=product, headers=self.headers
            )
            response.raise_for_status()
            print(f"✅ Created product: {product['name']}")
            return True
        except Exception as e:
            print(f"❌ Error creating {product['name']}: {str(e)}")
            if isinstance(e, httpx.HTTPStatusError):
                print(
                    f"For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{e.response.status_code}"
                )
            return False

    async def get_products(self, client: httpx.AsyncClient) -> list:
        """Get all products"""
        try:
            response = await client.get(f"{API_BASE_URL}/products")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting products: {str(e)}")
            return []


# Sample products data
PRODUCTS = [
    {
        "name": "MacBook Pro M3",
        "brand": "Apple",
        "model": "MBP16-M3-2024",
        "description": "16-inch MacBook Pro with M3 Pro chip, perfect for professional work and content creation",
        "price": 2499.99,
        "stock": 15,
        "warrantyPeriod": 12,
        "releaseDate": int((datetime.now() + timedelta(days=30)).timestamp() * 1000),
        "category": "Computacion",
        "productType": "Laptop",
        "processor": "Apple M3 Pro",
        "ram": "32GB",
        "storageType": "SSD",
        "storageCapacity": "1TB",
        "graphicsCard": "Integrated M3 Pro",
        "operatingSystem": "macOS",
        "specifications": {},
        "images": {},
    },
    {
        "name": "ThinkPad X1 Carbon",
        "brand": "Lenovo",
        "model": "X1C-2024",
        "description": "Ultra-light business laptop with premium features and security",
        "price": 1799.99,
        "stock": 20,
        "warrantyPeriod": 36,
        "releaseDate": int(datetime.now().timestamp() * 1000),
        "category": "Computacion",
        "productType": "Laptop",
        "processor": "Intel i7-1360P",
        "ram": "16GB",
        "storageType": "NVMe SSD",
        "storageCapacity": "512GB",
        "graphicsCard": "Intel Iris Xe",
        "operatingSystem": "Windows 11 Pro",
        "specifications": {},
        "images": {},
    },
    {
        "name": "HP LaserJet Pro",
        "brand": "HP",
        "model": "M404dn",
        "description": "Professional monochrome laser printer for business use",
        "price": 349.99,
        "stock": 25,
        "warrantyPeriod": 12,
        "releaseDate": int(datetime.now().timestamp() * 1000),
        "category": "Impresoras",
        "productType": "Printer",
        "printingTechnology": "Laser",
        "connectivityOptions": ["USB", "Ethernet", "WiFi"],
        "specifications": {},
        "images": {},
    },
]


async def main():
    api = ProductAPI()
    async with httpx.AsyncClient() as client:
        # First authenticate
        if not await api.login(client):
            print("Failed to authenticate. Exiting.")
            return

        # Create products
        print("\nCreating products...")
        for product in PRODUCTS:
            await api.create_product(client, product)

        # Verify products
        print("\nVerifying products...")
        products = await api.get_products(client)
        print("\nCurrent products in database:")
        print(json.dumps(products, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
