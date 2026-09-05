import csv
from typing import List, Dict
from models import Product, Order

def load_products(path: str) -> Dict[str, Product]:
    products: Dict[str, Product] = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prod = Product(
                product_id=row['product_id'],
                name=row['product_name'],
                category=row['category'],
                price=float(row['price'])
            )
            products[prod.product_id] = prod
    return products

def load_inventory(path: str) -> Dict[str, int]:
    inventory: Dict[str, int] = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert via float first to handle strings like "50.0"
            inventory[row['product_id']] = int(float(row['stock']))
    return inventory

def load_orders(path: str) -> List[Order]:
    orders: List[Order] = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            orders.append(Order(
                order_id=row['order_id'],
                product_id=row['product_id'],
                quantity=int(row['quantity']),
                date=row['date']
            ))
    return orders


