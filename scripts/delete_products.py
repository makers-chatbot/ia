import httpx
import asyncio
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

    async def get_products(self) -> list:
        """Get all products"""
        try:
            if not self.token:
                print("❌ Not authenticated. Please login first.")
                return []

            async with httpx.AsyncClient() as client:
                print("📋 Fetching products list...")
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

    async def delete_product(self, product_id: str) -> bool:
        """Delete a single product by ID"""
        try:
            if not self.token:
                print("❌ Not authenticated. Please login first.")
                return False

            async with httpx.AsyncClient() as client:
                print(f"🗑️  Deleting product with ID: {product_id}")
                response = await client.delete(
                    f"{self.base_url}/products/{product_id}", headers=self.headers
                )
                response.raise_for_status()
                print(f"✅ Deleted product: {product_id}")
                return True
        except httpx.HTTPStatusError as e:
            print(
                f"❌ HTTP Error deleting product {product_id}: {e.response.status_code}"
            )
            print(f"Response text: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error deleting product {product_id}: {str(e)}")
            if hasattr(e, "response") and e.response:
                print(f"Response text: {e.response.text}")
            return False


async def main():
    api = ProductAPI()

    # Login first
    if not await api.login():
        print("❌ Failed to authenticate. Exiting.")
        return

    # Get all products
    print("\nFetching products...")
    products = await api.get_products()

    if not products:
        print("No products found to delete.")
        return

    print(f"\nFound {len(products)} products to delete:")
    for product in products:
        print(f"- {product['name']} (ID: {product['id']})")

    # Delete each product
    print("\nDeleting products...")
    for product in products:
        await api.delete_product(product["id"])

    # Verify products were deleted
    remaining_products = await api.get_products()
    if not remaining_products:
        print("\n✅ All products successfully deleted!")
    else:
        print(f"\n⚠️  {len(remaining_products)} products still remain in the database.")


if __name__ == "__main__":
    asyncio.run(main())
