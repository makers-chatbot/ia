import httpx
import asyncio
from datetime import datetime, timedelta
import json

# Configuration
API_BASE_URL = "http://localhost:8081/api"
AUTH_CREDENTIALS = {"username": "admin", "password": "admin"}


class ProductAPI:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}

    async def login(self) -> bool:
        """Login to get authentication token"""
        try:
            async with httpx.AsyncClient() as client:
                print(
                    f"🔑 Attempting to login with credentials: {AUTH_CREDENTIALS['username']}"
                )
                response = await client.post(
                    f"{self.base_url}/auth/login", json=AUTH_CREDENTIALS
                )
                response.raise_for_status()
                data = response.json()
                print(f"🔄 Login response: {json.dumps(data, indent=2)}")

                if "token" not in data:
                    print("❌ No token field in response")
                    return False

                self.token = data["token"]
                self.headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}",
                }
                print("✅ Successfully authenticated")
                print(f"🔑 Token: {self.token[:20]}...")
                print(f"📋 Headers: {self.headers}")

                # Verify roles
                roles = data.get("userDTO", {}).get("rolesNames", [])
                print(f"👤 User roles: {roles}")
                if "ADMIN" not in roles:
                    print("❌ User does not have ADMIN role")
                    return False

                return True
        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP Error during authentication: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during authentication: {str(e)}")
            if hasattr(e, "response") and e.response:
                print(f"Response text: {e.response.text}")
            return False

    async def create_product(self, product: dict) -> bool:
        """Create a single product"""
        try:
            if not self.token:
                print("❌ Not authenticated. Please login first.")
                return False

            async with httpx.AsyncClient() as client:
                print(f"📦 Creating product: {product['name']}")
                print(f"Headers: {self.headers}")
                print(f"Product data: {json.dumps(product, indent=2)}")
                response = await client.post(
                    f"{self.base_url}/products", json=product, headers=self.headers
                )
                response.raise_for_status()
                print(f"✅ Created product: {product['name']}")
                return True
        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP Error creating {product['name']}: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error creating {product['name']}: {str(e)}")
            if hasattr(e, "response") and e.response:
                print(f"Response text: {e.response.text}")
            return False

    async def get_products(self) -> list:
        """Get all products"""
        try:
            if not self.token:
                print("❌ Not authenticated. Please login first.")
                return []

            async with httpx.AsyncClient() as client:
                print("📋 Fetching products list...")
                print(f"Headers: {self.headers}")
                response = await client.get(
                    f"{self.base_url}/products", headers=self.headers
                )
                response.raise_for_status()
                products = response.json()
                print(f"✅ Found {len(products)} products")
                return products
        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP Error getting products: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error getting products: {str(e)}")
            if hasattr(e, "response") and e.response:
                print(f"Response text: {e.response.text}")
            return []


async def main():
    # Sample products to create
    products = [
        {
            "name": "MacBook Pro M3",
            "brand": "Apple",
            "model": "2023",
            "description": "14-inch MacBook Pro with M3 chip",
            "price": 1599.99,
            "stock": 50,
            "warrantyPeriod": 12,
            "releaseDate": int(
                (datetime.now() + timedelta(days=365)).timestamp() * 1000
            ),
            "category": "Computacion",
            "productType": "Laptop",
            "processor": "Apple M3",
            "ram": "16GB",
            "storageType": "SSD",
            "storageCapacity": "512GB",
            "graphicsCard": "Apple M3 GPU",
            "operatingSystem": "macOS",
            "images": {
                "front": "https://midatlanticconsulting.com/blog/wp-content/uploads/2023/10/MacBook-Pro-Space-Black-M3-Pro.png"
            },
        },
        {
            "name": "ThinkPad X1 Carbon",
            "brand": "Lenovo",
            "model": "2023",
            "description": "14-inch ThinkPad X1 Carbon Gen 11",
            "price": 1399.99,
            "stock": 30,
            "warrantyPeriod": 12,
            "releaseDate": int(
                (datetime.now() + timedelta(days=365)).timestamp() * 1000
            ),
            "category": "Computacion",
            "productType": "Laptop",
            "processor": "Intel i7-1355U",
            "ram": "16GB",
            "storageType": "SSD",
            "storageCapacity": "1TB",
            "graphicsCard": "Intel Iris Xe",
            "operatingSystem": "Windows 11 Pro",
            "images": {
                "front": "https://notebooks.com/wp-content/uploads/2012/12/X1_Carbon-Touch_hero_05.jpg"
            },
        },
        {
            "name": "HP LaserJet Pro",
            "brand": "HP",
            "model": "M404dn",
            "description": "Professional monochrome laser printer",
            "price": 299.99,
            "stock": 20,
            "warrantyPeriod": 12,
            "releaseDate": int(
                (datetime.now() + timedelta(days=365)).timestamp() * 1000
            ),
            "category": "Impresion",
            "productType": "Printer",
            "printingTechnology": "Laser",
            "connectivityOptions": ["USB", "Ethernet", "Wi-Fi"],
            "images": {
                "front": "https://www.bhphotovideo.com/images/images2500x2500/hp_cf399a_bgj_laserjet_pro_400_m401dne_994419.jpg"
            },
        },
        {
            "name": "Dell XPS 15",
            "brand": "Dell",
            "model": "9530",
            "description": "15.6-inch premium laptop with OLED display",
            "price": 1899.99,
            "stock": 25,
            "warrantyPeriod": 12,
            "releaseDate": int(
                (datetime.now() + timedelta(days=365)).timestamp() * 1000
            ),
            "category": "Computacion",
            "productType": "Laptop",
            "processor": "Intel i9-13900H",
            "ram": "32GB",
            "storageType": "SSD",
            "storageCapacity": "1TB",
            "graphicsCard": "NVIDIA RTX 4070",
            "operatingSystem": "Windows 11 Pro",
            "images": {
                "front": "https://tech.co.za/wp-content/uploads/2022/06/Dell-XSP-15-9520-v2.png"
            },
        },
        {
            "name": "ASUS ROG Zephyrus G14",
            "brand": "ASUS",
            "model": "2024",
            "description": "14-inch gaming laptop with AMD Ryzen processor",
            "price": 1699.99,
            "stock": 20,
            "warrantyPeriod": 12,
            "releaseDate": int(
                (datetime.now() + timedelta(days=365)).timestamp() * 1000
            ),
            "category": "Computacion",
            "productType": "Laptop",
            "processor": "AMD Ryzen 9 7940HS",
            "ram": "32GB",
            "storageType": "SSD",
            "storageCapacity": "1TB",
            "graphicsCard": "NVIDIA RTX 4060",
            "operatingSystem": "Windows 11 Pro",
            "images": {
                "front": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6403/6403816cv1d.jpg"
            },
        },
    ]

    api = ProductAPI()

    # Login first
    if not await api.login():
        print("❌ Failed to authenticate. Exiting.")
        return

    # Create products
    print("\nCreating products...")
    for product in products:
        await api.create_product(product)

    # Verify products were created
    print("\nVerifying products...")
    current_products = await api.get_products()
    print("\nCurrent products in database:")
    print(json.dumps(current_products, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
