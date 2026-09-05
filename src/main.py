import os
import csv
import pandas as pd

from utils import load_products, load_inventory, load_orders
from inventory_manager import InventoryManager
from auth import login, logout

import seaborn as sns
import matplotlib.pyplot as plt

# Professional theme
sns.set_theme(style="whitegrid", palette="pastel")

# Paths to your CSVs
BASE_DIR      = os.path.join(os.path.dirname(__file__), '..', 'data')
PRODUCTS_CSV  = os.path.join(BASE_DIR, 'products.csv')
INVENTORY_CSV = os.path.join(BASE_DIR, 'inventory.csv')
ORDERS_CSV    = os.path.join(BASE_DIR, 'orders.csv')

def add_item():
    """Add a new product to products.csv & inventory.csv"""
    print("\n🆕 Add a New Product")
    pid   = input(" Product ID: ").strip()
    name  = input(" Name      : ").strip()
    cat   = input(" Category  : ").strip()
    price = input(" Price     : ").strip()
    stock = input(" Stock     : ").strip()

    with open(PRODUCTS_CSV, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([pid, name, cat, price])
    with open(INVENTORY_CSV, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([pid, stock])

    print(f"✅ Product {pid} added.\n")

def delete_item():
    """Delete a product (and its inventory)"""
    pid = input("\n🗑️ Delete Product ID: ").strip()
    df = pd.read_csv(PRODUCTS_CSV)
    df = df[df.product_id != pid]
    df.to_csv(PRODUCTS_CSV, index=False)

    df_inv = pd.read_csv(INVENTORY_CSV)
    df_inv = df_inv[df_inv.product_id != pid]
    df_inv.to_csv(INVENTORY_CSV, index=False)

    print(f"✅ Product {pid} deleted.\n")

def list_items():
    """Display all products with their current stock and price"""
    df = pd.read_csv(PRODUCTS_CSV)
    df_inv = pd.read_csv(INVENTORY_CSV)
    merged = df.merge(df_inv, on="product_id")
    print("\n📦 All Products:\n", merged.to_string(index=False), "\n")

def add_order():
    """Add a new order to orders.csv"""
    print("\n🆕 Add a New Order")
    oid  = input(" Order ID  : ").strip()
    pid  = input(" Product ID: ").strip()
    qty  = input(" Quantity  : ").strip()
    date = input(" Date (YYYY-MM-DD): ").strip()

    with open(ORDERS_CSV, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([oid, pid, qty, date])
    print(f"✅ Order {oid} added.\n")

def delete_order():
    """Delete an order from orders.csv"""
    oid = input("\n🗑️ Delete Order ID: ").strip()
    df = pd.read_csv(ORDERS_CSV)
    df = df[df.order_id != oid]
    df.to_csv(ORDERS_CSV, index=False)
    print(f"✅ Order {oid} deleted.\n")

def list_orders():
    """Display all orders with product names and current stock"""
    df_o = pd.read_csv(ORDERS_CSV)
    df_p = pd.read_csv(PRODUCTS_CSV)
    df_i = pd.read_csv(INVENTORY_CSV)
    merged = df_o.merge(df_p, on="product_id").merge(df_i, on="product_id")
    print("\n📝 All Orders:\n", merged.to_string(index=False), "\n")

def analyze():
    """Generate and display 3-panel sales dashboard"""

    # 1) Reload all data
    products  = load_products(PRODUCTS_CSV)
    inventory = load_inventory(INVENTORY_CSV)
    orders    = load_orders(ORDERS_CSV)

    mgr = InventoryManager(products, inventory)
    mgr.process_orders(orders)

    # 2) Prepare data
    all_sales = mgr.sales_count
    names_all = list(all_sales.keys())
    values_all= list(all_sales.values())

    top5 = mgr.get_top_sellers(top_n=5)
    names5    = [p.name for p, _ in top5]
    values5   = [qty for _, qty in top5]

    cat_rev = mgr.revenue_by_category()
    labels_p = list(cat_rev.keys())
    values_p = list(cat_rev.values())

    # 3) Build a 1x3 subplot grid
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

    # --- Subplot 1: All‑Products Bar Chart ---
    ax1 = axes[0]
    sns.barplot(x=values_all, y=names_all, ax=ax1)
    ax1.set_title("Units Sold by Product")
    ax1.set_xlabel("Units Sold")
    ax1.set_ylabel("Product ID")
    for i, v in enumerate(values_all):
        ax1.text(v + 0.5, i, str(v), va='center')

    # --- Subplot 2: Top‑5 Sellers Bar Chart ---
    ax2 = axes[1]
    sns.barplot(x=values5, y=names5, ax=ax2)
    ax2.set_title("Top-5 Selling Products")
    ax2.set_xlabel("Units Sold")
    ax2.set_ylabel("Product Name")
    for i, v in enumerate(values5):
        ax2.text(v + 0.5, i, str(v), va='center')

    # --- Subplot 3: Revenue‑Share Pie Chart ---
    ax3 = axes[2]
    ax3.pie(
        values_p,
        labels=labels_p,
        autopct='%1.1f%%',
        startangle=140,
        shadow=True
    )
    ax3.set_title("Revenue Share by Category")

    # 4) Final layout and render
    plt.tight_layout()
    plt.show()

def menu():
    """Display the main menu and handle user choices"""
    while True:
        print(
            "\n📊 Main Menu\n"
            "1) Items   2) Orders   3) Analyze   4) Logout\n"
        )
        choice = input("Choose an option [1-4]: ").strip()
        if choice == '1':
            list_items()
            sub = input(" (A)dd or (D)elete item? (A/D/N): ").strip().upper()
            if sub == 'A': add_item()
            elif sub == 'D': delete_item()
        elif choice == '2':
            list_orders()
            sub = input(" (A)dd or (D)elete order? (A/D/N): ").strip().upper()
            if sub == 'A': add_order()
            elif sub == 'D': delete_order()
        elif choice == '3':
            analyze()
        elif choice == '4':
            logout()
            break
        else:
            print("❌ Invalid choice, please select 1–4.")

if __name__ == '__main__':
    if not login():
        exit(1)
    menu()
