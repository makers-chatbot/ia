from product_client import ProductClient, logger
import asyncio


class InventoryManager:
    def __init__(self):
        logger.info("Initializing InventoryManager")
        self.product_client = ProductClient()

    async def get_product_list(self) -> str:
        """Get the formatted product list with all details"""
        logger.info("Getting formatted product list")

        # Fetch products from the backend
        products = await self.product_client.get_products()

        if not products:
            logger.warning("No products returned from backend")
            return "Sorry, I couldn't retrieve the product list at the moment."

        logger.info(f"Formatting {len(products)} products")
        formatted = "Available Products:\n\n"

        try:
            for p in products:
                logger.debug(f"Formatting product: {p.name}")
                formatted += f"• {p.name} ({p.brand} {p.model})\n"
                formatted += f"  Description: {p.description}\n"
                formatted += f"  Category: {p.category}\n"
                formatted += f"  Price: ${p.price:,.2f}\n"
                formatted += f"  Stock: {p.stock} units\n"

                # Add category-specific details
                if p.processor:  # Computer specific
                    formatted += f"  Processor: {p.processor}\n"
                    formatted += f"  RAM: {p.ram}\n"
                    formatted += f"  Storage: {p.storageCapacity} {p.storageType}\n"
                    formatted += f"  Graphics: {p.graphicsCard}\n"
                    formatted += f"  OS: {p.operatingSystem}\n"
                elif p.printingTechnology:  # Printer specific
                    formatted += f"  Printing Technology: {p.printingTechnology}\n"
                    if p.connectivityOptions:
                        formatted += (
                            f"  Connectivity: {', '.join(p.connectivityOptions)}\n"
                        )

                formatted += "\n"

            logger.info("Successfully formatted all products")
            return formatted

        except Exception as e:
            logger.error(f"Error formatting products: {str(e)}", exc_info=True)
            return "Sorry, there was an error formatting the product list."

    # Commented out old hardcoded products
    """
    @staticmethod
    def get_product_list() -> str:
        products = [
            Product(
                name="Dell XPS 13",
                description="High-end ultrabook with 13-inch display",
                price=1299.99,
            ),
            Product(
                name="MacBook Pro M2",
                description="Professional laptop with Apple Silicon",
                price=1999.99,
            ),
            Product(
                name="ThinkPad X1",
                description="Business laptop with excellent keyboard",
                price=1499.99,
            ),
            Product(
                name="HP Spectre x360",
                description="Premium convertible laptop",
                price=1399.99,
            ),
        ]
    """


async def main():
    # Create inventory manager
    inventory = InventoryManager()

    try:
        # Get and print the product list
        logger.info("=== Starting product list test ===")
        product_list = await inventory.get_product_list()
        print("=== Product List from Backend API ===")
        print(product_list)
        logger.info("=== Product list test completed ===")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        print(f"Error getting product list: {e}")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
