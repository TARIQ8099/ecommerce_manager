import csv
import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox, simpledialog

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Segoe UI Emoji'
from utils import load_products, load_inventory, load_orders
from inventory_manager import InventoryManager
from auth import USERS

# Paths
BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
PRODUCTS_CSV = os.path.join(BASE_DIR, 'products.csv')
INVENTORY_CSV = os.path.join(BASE_DIR, 'inventory.csv')
ORDERS_CSV = os.path.join(BASE_DIR, 'orders.csv')

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Commerce Manager")
        self.geometry("1200x800")
        self.resizable(False, False)

        # — Professional Color Theme Setup —
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('LoginFrame.TFrame', background='#e3f2fd')
        style.configure(
            'Header.TLabel',
            background='#e3f2fd',
            foreground='#0d47a1',
            font=('Segoe UI', 26, 'bold')
        )
        style.configure(
            'Field.TLabel',
            background='#e3f2fd',
            foreground='#0d47a1',
            font=('Segoe UI', 14)
        )
        style.configure('TEntry', fieldbackground='white', background='white', padding=5)
        style.configure(
            'Login.TButton',
            background='#1976d2',
            foreground='white',
            font=('Segoe UI', 14, 'bold'),
            padding=(10, 5)
        )
        style.map(
            'Login.TButton',
            background=[('active', '#1565c0'), ('pressed', '#0d47a1')],
            foreground=[('disabled', '#aaa')]
        )

        style = ttk.Style()
        style.theme_use('clam')  # Optional: Use a cleaner look

        style.configure('MainMenu.TFrame', background='#e3f2fd')  # light blue background
        style.configure('MenuLabel.TLabel', font=('Segoe UI', 26, 'bold'), background='#e3f2fd', foreground='#0d47a1')
        style.configure('MenuButton.TButton', font=('Segoe UI', 15, 'bold'), padding=12)
        style.map('MenuButton.TButton', background=[('active', '#1565c0')])

        style = ttk.Style()
        style.theme_use('clam')

        # Frame + title styling
        style.configure('InventoryFrame.TFrame', background='#fffde7')  # light yellow
        style.configure('InventoryTitle.TLabel', font=('Segoe UI', 24, 'bold'), foreground='#f57f17',
                        background='#fffde7')

        # Treeview style
        style.configure('Treeview', font=('Segoe UI', 11), rowheight=30)
        style.configure('Treeview.Heading', font=('Segoe UI', 12, 'bold'), foreground='#fff', background='#f57f17')
        style.map('Treeview', background=[('selected', '#ffecb3')])

        # Button styling
        style.configure('Inventory.TButton', font=('Segoe UI', 12, 'bold'), padding=10)
        style.map('Inventory.TButton', background=[('active', '#ffb300')])

        # Override Tkinter's default font so that all widgets can render emojis
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI Emoji", size=12)

        # Also bump button and label defaults if you like
        tkFont.nametofont("TkTextFont").configure(family="Segoe UI Emoji", size=12)
        tkFont.nametofont("TkMenuFont").configure(family="Segoe UI Emoji", size=12)

        self.show_login()

    def clear_frame(self):
        """
        Destroy all child widgets of this window.
        """
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_frame()

        # 0) Outer container to help center everything
        outer_frame = ttk.Frame(self)
        outer_frame.pack(expand=True, fill='both')  # Takes full space

        # 1) Inner styled frame, centered using grid inside outer_frame
        frame = ttk.Frame(outer_frame, style='LoginFrame.TFrame', padding=30)
        frame.grid(row=0, column=0)

        outer_frame.rowconfigure(0, weight=1)
        outer_frame.columnconfigure(0, weight=1)

        # 2) Header in bold dark blue
        ttk.Label(
            frame,
            text="🔐 Login Required",
            style='Header.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # 3) Username field label
        ttk.Label(
            frame,
            text="Username:",
            style='Field.TLabel'
        ).grid(row=1, column=0, sticky="e", padx=5, pady=5)

        user = ttk.Entry(frame)
        user.grid(row=1, column=1, pady=5, ipadx=10, ipady=5)

        # 4) Password field label
        ttk.Label(
            frame,
            text="Password:",
            style='Field.TLabel'
        ).grid(row=2, column=0, sticky="e", padx=5, pady=5)

        pwd = ttk.Entry(frame, show="*")
        pwd.grid(row=2, column=1, pady=5, ipadx=10, ipady=5)

        # 5) Styled Login button
        def attempt_login():
            if USERS.get(user.get()) == pwd.get():
                messagebox.showinfo("✅ Login", "Login Successful!")
                self.show_menu()
            else:
                messagebox.showerror("❌ Login", "Invalid credentials")

        ttk.Button(
            frame,
            text="Login",
            style='Login.TButton',
            command=attempt_login
        ).grid(row=3, column=0, columnspan=2, pady=(20, 0))

    def show_menu(self):
        self.clear_frame()

        # Outer frame with custom background
        frame = ttk.Frame(self, style='MainMenu.TFrame')
        frame.pack(expand=True, fill='both')

        # Make center-aligned grid
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Inner content frame
        inner = ttk.Frame(frame, style='MainMenu.TFrame')
        inner.grid(row=0, column=0)

        # Title label
        ttk.Label(
            inner,
            text="📊 Welcome to Your Dashboard",
            style='MenuLabel.TLabel'
        ).pack(pady=(50, 30))

        # Buttons with better labels + emojis
        buttons = [
            ("🧾 Manage Inventory", self.show_items),
            ("📦 View Sales Orders", self.show_orders),
            ("📈 Sales Analytics", self.show_analyze),
            ("🔒 Logout", self.show_login)
        ]

        for text, command in buttons:
            ttk.Button(inner, text=text, command=command, style='MenuButton.TButton').pack(
                pady=12, ipadx=10, ipady=5
            )

    def show_items(self):
        self.clear_frame()
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frame, text="🛒 Inventory Manager", style='MainLabel.TLabel').pack(pady=(10, 20))

        cols = ['product_id', 'product_name', 'category', 'price', 'stock']
        tree = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            tree.heading(c, text=c.replace('_', ' ').title())
            tree.column(c, width=150)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_items(tree)

        btns = ttk.Frame(frame)
        btns.pack(pady=15)
        ttk.Button(btns, text="➕ Add Item", style='Item.TButton', command=lambda: self.add_item(tree)).pack(side="left",
                                                                                                            padx=10)
        ttk.Button(btns, text="🗑 Delete Item", style='Item.TButton', command=lambda: self.delete_item(tree)).pack(
            side="left", padx=10)
        ttk.Button(btns, text="🔙 Back", style='Item.TButton', command=self.show_menu).pack(side="left", padx=10)

    def refresh_items(self, tree):
        for r in tree.get_children(): tree.delete(r)
        df = pd.read_csv(PRODUCTS_CSV).merge(pd.read_csv(INVENTORY_CSV), on="product_id")
        for _, row in df.iterrows():
            tree.insert("", "end", values=(row['product_id'], row['product_name'], row['category'], row['price'], row['stock']))

    def add_item(self, tree):
        entries = [
            ("Product ID", str), ("Name", str), ("Category", str),
            ("Price", float), ("Stock", int)
        ]
        data = []
        for prompt, _type in entries:
            val = simpledialog.askstring("Add Item", prompt, parent=self)
            if val is None: return
            data.append(val)
        # write
        with open(PRODUCTS_CSV, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(data[:4])
        with open(INVENTORY_CSV, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([data[0], data[4]])
        self.refresh_items(tree)

    def delete_item(self, tree):
        sel = tree.selection()
        if not sel: return
        pid = tree.item(sel[0])['values'][0]
        df = pd.read_csv(PRODUCTS_CSV); df = df[df.product_id != pid]; df.to_csv(PRODUCTS_CSV, index=False)
        df2 = pd.read_csv(INVENTORY_CSV); df2 = df2[df2.product_id != pid]; df2.to_csv(INVENTORY_CSV, index=False)
        self.refresh_items(tree)

    def show_orders(self):
        self.clear_frame()
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frame, text="📦 Orders Manager", style='MainLabel.TLabel').pack(pady=(10, 20))

        cols = ['order_id', 'product_id', 'quantity', 'date', 'stock']
        tree = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            tree.heading(c, text=c.replace('_', ' ').title())
            tree.column(c, width=130)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_orders(tree)

        btns = ttk.Frame(frame)
        btns.pack(pady=15)
        ttk.Button(btns, text="➕ Add Order", style='Item.TButton', command=lambda: self.add_order(tree)).pack(
            side="left", padx=10)
        ttk.Button(btns, text="🗑 Delete Order", style='Item.TButton', command=lambda: self.delete_order(tree)).pack(
            side="left", padx=10)
        ttk.Button(btns, text="🔙 Back", style='Item.TButton', command=self.show_menu).pack(side="left", padx=10)

    def refresh_orders(self, tree):
        for r in tree.get_children():
            tree.delete(r)
        df_o = pd.read_csv(ORDERS_CSV)
        df_p = pd.read_csv(PRODUCTS_CSV)
        df_i = pd.read_csv(INVENTORY_CSV)
        merged = df_o.merge(df_p, on="product_id").merge(df_i, on="product_id")
        for _, r in merged.iterrows():
            tree.insert("", "end", values=(r['order_id'], r['product_id'], r['quantity'], r['date'], r['stock']))

    def add_order(self, tree):
        prompts = [("Order ID", str), ("Product ID", str), ("Quantity", int), ("Date YYYY-MM-DD", str)]
        data = []
        for prompt, _type in prompts:
            val = simpledialog.askstring("Add Order", prompt, parent=self)
            if val is None: return
            data.append(val)
        with open(ORDERS_CSV, 'a', newline='') as f:
            csv.writer(f).writerow(data)
        self.refresh_orders(tree)

    def delete_order(self, tree):
        sel = tree.selection()
        if not sel:
            return
        # 1) Get selected Order ID
        oid = tree.item(sel[0])['values'][0]

        # 2) Read all orders from CSV
        with open(ORDERS_CSV, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            orders = [row for row in reader if row['order_id'] != str(oid)]

        # 3) Write back filtered orders
        with open(ORDERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['order_id', 'product_id', 'quantity', 'date'])
            writer.writeheader()
            writer.writerows(orders)

        # 4) Refresh the Treeview
        self.refresh_orders(tree)

    def show_analyze(self):
        """Open a bright, professional Analyze Dashboard with clear visuals."""
        import matplotlib.pyplot as plt
        import seaborn as sns
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        # Load data
        products = load_products(PRODUCTS_CSV)
        inventory = load_inventory(INVENTORY_CSV)
        orders = load_orders(ORDERS_CSV)

        mgr = InventoryManager(products, inventory)
        mgr.process_orders(orders)

        # Create new analysis window
        win = tk.Toplevel(self)
        win.title("📊 Sales & Inventory Insights")
        win.geometry("1000x720")
        win.configure(bg="#ffffff")  # Bright white background

        # Notebook for tabs
        notebook = ttk.Notebook(win)
        notebook.pack(expand=1, fill='both', padx=12, pady=12)

        # ===== TAB 1: Units Sold by Product =====
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Units Sold")

        fig1, ax1 = plt.subplots(figsize=(9, 5))
        sns.set(style="whitegrid")
        data_all = mgr.sales_count
        names_all = list(data_all.keys())
        vals_all = list(data_all.values())

        sns.barplot(x=vals_all, y=names_all, ax=ax1, hue=names_all, palette="Spectral", legend=False)
        ax1.set_title("Units Sold by Product", fontsize=17, fontweight='bold', color="#1a1a1a")
        ax1.set_xlabel("Units Sold", fontsize=13)
        ax1.set_ylabel("Product ID", fontsize=13)
        for i, v in enumerate(vals_all):
            ax1.text(v + 1, i, str(v), va='center', fontsize=11, color="#333333")
        fig1.tight_layout()
        FigureCanvasTkAgg(fig1, master=tab1).get_tk_widget().pack(expand=1, fill='both')

        # ===== TAB 2: Revenue Share by Category =====
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Revenue Share")

        fig2, ax2 = plt.subplots(figsize=(8, 5))
        data_cat = mgr.revenue_by_category()
        labels = list(data_cat.keys())
        sizes = list(data_cat.values())
        bright_colors = sns.color_palette("Set3", len(labels))
        ax2.pie(
            sizes, labels=labels, autopct=lambda pct: f"{pct:.1f}%",
            startangle=140, shadow=False, colors=bright_colors,
            textprops={'fontsize': 11, 'color': '#000000'}
        )
        ax2.set_title("Revenue Share by Category", fontsize=17, fontweight='bold', color="#1a1a1a")
        fig2.tight_layout()
        FigureCanvasTkAgg(fig2, master=tab2).get_tk_widget().pack(expand=1, fill='both')

        # ===== TAB 3: Top 5 Selling Products =====
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Top Sellers")

        fig3, ax3 = plt.subplots(figsize=(9, 5))
        top5 = mgr.get_top_sellers(top_n=5)
        names5 = [p.name for p, _ in top5]
        vals5 = [qty for _, qty in top5]

        sns.barplot(x=vals5, y=names5, ax=ax3, hue=names5, palette="YlOrRd", legend=False)
        ax3.set_title("Top 5 Selling Products", fontsize=17, fontweight='bold', color="#1a1a1a")
        ax3.set_xlabel("Units Sold", fontsize=13)
        ax3.set_ylabel("Product Name", fontsize=13)
        for i, v in enumerate(vals5):
            ax3.text(v + 1, i, str(v), va='center', fontsize=11, color="#333333")
        fig3.tight_layout()
        FigureCanvasTkAgg(fig3, master=tab3).get_tk_widget().pack(expand=1, fill='both')

if __name__ == '__main__':
    App().mainloop()
