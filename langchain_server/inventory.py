from models import Product


class InventoryManager:
    @staticmethod
    def get_product_list() -> str:
        """Get the formatted product list with all details"""
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

        formatted = "Available Products:\n\n"
        for p in products:
            formatted += f"• {p.name}\n"
            formatted += f"  Description: {p.description}\n"
            formatted += f"  Price: ${p.price:,.2f}\n\n"
        return formatted
