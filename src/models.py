from dataclasses import dataclass

@dataclass
class Product:
    product_id: str
    name: str
    category: str
    price: float

@dataclass
class Order:
    order_id: str
    product_id: str
    quantity: int
    date: str

