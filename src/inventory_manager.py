from typing import Dict, List
from models import Product, Order

# Threshold for low‑stock alerts
LOW_STOCK_THRESHOLD = 10
class InventoryManager:
    def __init__(self, products: Dict[str, Product], inventory: Dict[str, int]):
        """
        products: map product_id -> Product
        inventory: map product_id -> available stock
        """
        # Store inputs
        self.products = products
        self.inventory = inventory

        # Initialize running totals
        self.revenue: float = 0.0
        self.sales_count: Dict[str, int] = {}

    def process_orders(self, orders: List[Order]):
        """
        Process each Order:
        1. Check if in inventory
        2. Check stock sufficiency
        3. Deduct stock
        4. Update revenue
        5. Track sales
        6. Alert low stock
        """
        for order in orders:
            pid = order.product_id
            qty = order.quantity

            # 1) Existence check
            if pid not in self.inventory:
                print(f"Warning: {pid} not in inventory.")
                continue

            # 2) Stock check
            if self.inventory[pid] < qty:
                print(f"Insufficient stock for {pid}: have {self.inventory[pid]}, order {qty}")
                continue

            # 3) Deduct stock
            self.inventory[pid] -= qty

            # 4) Update revenue
            price = self.products[pid].price
            self.revenue += price * qty

            # 5) Track sales
            self.sales_count[pid] = self.sales_count.get(pid, 0) + qty

            # 6) Low‑stock alert
            if self.inventory[pid] <= LOW_STOCK_THRESHOLD:
                print(f"Low stock alert: {pid} has {self.inventory[pid]} units left.")

    def get_top_sellers(self, top_n: int = 5):
        """
        Return a list of (Product, qty) tuples for the top N sellers.
        """
        # Sort by sold quantity descending
        sorted_sales = sorted(
            self.sales_count.items(),
            key=lambda item: item[1],
            reverse=True
        )
        # Map to (Product, qty)
        return [(self.products[pid], qty) for pid, qty in sorted_sales[:top_n]]

    def revenue_by_category(self):
        """
        Compute total revenue per product category.
        """
        category_rev: Dict[str, float] = {}
        for pid, qty in self.sales_count.items():
            cat = self.products[pid].category
            category_rev[cat] = category_rev.get(cat, 0.0) + self.products[pid].price * qty
        return category_rev





