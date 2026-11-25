from products import getproductdetails, getproducts, updateStock, saveHistory, load_all_products, load_sales_history
from tkinter import ttk, filedialog, messagebox
from screen import indian_format, clear, build_navbar
import tkinter as tk
from datetime import datetime


def navbtn(root, val):
    val_lower = val.lower().strip()
    clear(root)

    if val_lower == "home":
        dashboard(root)
    elif val_lower == "new bill":
        home(root)
    elif val_lower in ("product & stock", "product_stock"):
        from stock import productStock
        productStock(root)
    elif val_lower in ("sales history", "saleshistory"):
        from sales import salesHistory
        salesHistory(root)
    elif val_lower == "logout":
        from auth import signin
        signin(root)


def dashboard(root):
    """Home overview page showing key business metrics and quick actions."""
    root.title("Retail Billing & Inventory System - Home")
    root.geometry("1280x720")
    root.configure(bg="#F0F2F5")

    build_navbar(root, "Home", navbtn)

    products = load_all_products()
    sales = load_sales_history()

    today_str = datetime.now().strftime("%d-%m-%Y")
    total_revenue = sum(float(s.get("total", 0)) for s in sales)
    today_sales = [s for s in sales if str(s.get("date", "")).startswith(today_str)]
    today_revenue = sum(float(s.get("total", 0)) for s in today_sales)
    low_stock_items = [p for p in products if int(p.get("stock", 0)) <= 10]

    container = tk.Frame(root, bg="#F0F2F5")
    container.pack(fill="both", expand=True, padx=20, pady=15)

    # Top Summary Cards
    cards_frame = tk.Frame(container, bg="#F0F2F5")
    cards_frame.pack(fill="x", pady=(0, 15))
    for i in range(4):
        cards_frame.columnconfigure(i, weight=1, uniform="cards")

    cards = [
        ("Total Products", str(len(products)), "#1596FC"),
        ("Low Stock Alerts (≤10)", str(len(low_stock_items)), "#E67E22"),
        ("Today's Sales", f"₹{indian_format(today_revenue)}", "#27AE60"),
        ("Total Revenue", f"₹{indian_format(total_revenue)}", "#232E40"),
    ]

    for idx, (title, value, accent) in enumerate(cards):
        card = tk.Frame(cards_frame, bg="#FFFFFF", bd=1, relief="solid")
        card.grid(row=0, column=idx, padx=8, sticky="nsew")

        bar = tk.Frame(card, bg=accent, height=6)
        bar.pack(fill="x")

        tk.Label(card, text=title, font=("Segoe UI", 11), fg="#555555", bg="#FFFFFF").pack(anchor="w", padx=15, pady=(12, 4))
        tk.Label(card, text=value, font=("Segoe UI", 20, "bold"), fg="#232E40", bg="#FFFFFF").pack(anchor="w", padx=15, pady=(0, 15))

    # Middle Quick Action Bar
    action_frame = tk.LabelFrame(
        container, text="Quick Actions", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=15, pady=12
    )
    action_frame.pack(fill="x", pady=(0, 15))

    tk.Button(
        action_frame, text="+ Create New Bill", font=("Segoe UI", 12, "bold"),
        bg="#27AE60", fg="white", relief="flat", cursor="hand2",
        command=lambda: navbtn(root, "New Bill")
    ).pack(side="left", padx=(0, 12), ipadx=14, ipady=6)

    tk.Button(
        action_frame, text="Manage Products & Stock", font=("Segoe UI", 12, "bold"),
        bg="#1596FC", fg="white", relief="flat", cursor="hand2",
        command=lambda: navbtn(root, "Product & Stock")
    ).pack(side="left", padx=12, ipadx=14, ipady=6)

    tk.Button(
        action_frame, text="View Sales Reports", font=("Segoe UI", 12, "bold"),
        bg="#333F57", fg="white", relief="flat", cursor="hand2",
        command=lambda: navbtn(root, "Sales History")
    ).pack(side="left", padx=12, ipadx=14, ipady=6)

    # Bottom Split: Recent Sales & Low Stock Table
    bottom = tk.Frame(container, bg="#F0F2F5")
    bottom.pack(fill="both", expand=True)
    bottom.columnconfigure(0, weight=1, uniform="bottom")
    bottom.columnconfigure(1, weight=1, uniform="bottom")
    bottom.rowconfigure(0, weight=1)

    recent_frame = tk.LabelFrame(
        bottom, text="Recent Invoices", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    recent_frame.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

    r_cols = ("Invoice ID", "Date", "Customer", "Total")
    r_tree = ttk.Treeview(recent_frame, columns=r_cols, show="headings", height=10)
    for col in r_cols:
        r_tree.heading(col, text=col)
    r_tree.column("Invoice ID", width=165, anchor="w")
    r_tree.column("Date", width=120, anchor="center")
    r_tree.column("Customer", width=130, anchor="w")
    r_tree.column("Total", width=100, anchor="e")
    r_tree.pack(fill="both", expand=True)

    for s in reversed(sales[-10:]):
        r_tree.insert("", "end", values=(
            s.get("invoice_id", ""),
            s.get("date", ""),
            s.get("customer", {}).get("name", ""),
            f"₹{indian_format(s.get('total', 0))}"
        ))

    low_frame = tk.LabelFrame(
        bottom, text="Low Stock Products (Stock ≤ 10)", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    low_frame.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

    l_cols = ("ID", "Product Name", "Price", "Stock Left")
    l_tree = ttk.Treeview(low_frame, columns=l_cols, show="headings", height=10)
    for col in l_cols:
        l_tree.heading(col, text=col)
    l_tree.column("ID", width=70, anchor="center")
    l_tree.column("Product Name", width=210, anchor="w")
    l_tree.column("Price", width=100, anchor="e")
    l_tree.column("Stock Left", width=90, anchor="center")
    l_tree.pack(fill="both", expand=True)

    for p in sorted(low_stock_items, key=lambda x: int(x.get("stock", 0))):
        l_tree.insert("", "end", values=(
            p.get("id", ""),
            p.get("name", ""),
            f"₹{indian_format(p.get('price', 0))}",
            p.get("stock", 0)
        ))


def home(root):
    """Main Billing Screen (New Bill)."""
    root.title("Retail Billing & Inventory System - New Bill")
    root.geometry("1280x720")
    root.configure(bg="#F0F2F5")

    current_subtotal = tk.DoubleVar(value=0.0)

    def recalculate_subtotal():
        total_sub = 0.0
        for row in table.get_children():
            vals = table.item(row, "values")
            total_sub += float(vals[4])
        current_subtotal.set(total_sub)
        subamount.config(text=f"₹{indian_format(total_sub)}")

    def getInvoice(discount_amount, gst_amount, total_amount, invoice_id="PREVIEW"):
        dt = datetime.now().strftime("%d-%m-%Y %H:%M")
        cust_name = nameInput.get().strip() or "Walk-in Customer"
        cust_phone = phoneInput.get().strip() or "N/A"

        receipt = f"""
========================================
         RETAIL BILLING INVOICE
========================================
Invoice No : {invoice_id}
Date       : {dt}
Customer   : {cust_name}
Phone      : {cust_phone}
----------------------------------------
Item                  Qty      Amount
----------------------------------------
"""
        for item in table.get_children():
            product_id, name, price, quantity, amount = table.item(item, "values")
            receipt += (
                f"{name[:20]:<20} x{str(quantity):<4} "
                f"₹{indian_format(amount):>9}\n"
            )

        receipt += f"""----------------------------------------
Subtotal:                ₹{indian_format(current_subtotal.get()):>10}
Discount:               -₹{indian_format(discount_amount):>10}
Tax / GST:              +₹{indian_format(gst_amount):>10}
----------------------------------------
TOTAL:                   ₹{indian_format(total_amount):>10}
Payment Method: {methodInput.get()}
========================================
        THANK YOU FOR SHOPPING!
========================================
"""
        invoice.config(state="normal")
        invoice.delete("1.0", "end")
        invoice.insert("1.0", receipt.strip())
        invoice.config(state="disabled")

    def getTotal():
        try:
            if not table.get_children():
                messagebox.showwarning("Empty Cart", "Please add at least one item to calculate the bill.")
                return None

            sbtotal = current_subtotal.get()
            dctamount = float(discountInput.get() or 0)
            txgst = float(tax_gstInput.get() or 0)

            if not 0 <= dctamount <= 100:
                messagebox.showerror("Invalid Discount", "Discount must be between 0 and 100%.")
                return None
            if not 0 <= txgst <= 100:
                messagebox.showerror("Invalid GST", "GST must be between 0 and 100%.")
                return None

            discount = sbtotal * (dctamount / 100)
            gst = (sbtotal - discount) * (txgst / 100)
            totalamount = sbtotal - discount + gst
            total.config(text=f"Total: ₹{indian_format(totalamount)}")
            getInvoice(discount, gst, totalamount)
            return sbtotal, dctamount, discount, txgst, gst, totalamount

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
            return None

    def addItems():
        try:
            selected = dropdown.get()
            if selected == "Select product" or not selected:
                messagebox.showwarning("Select Product", "Please select a product first.")
                return

            product_id = selected.split("-")[0].strip()
            quantity = int(qty.get())
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")

            product = getproductdetails(product_id)
            if product is None:
                messagebox.showerror("Product Error", "Selected product was not found.")
                return

            staged_qty = 0
            existing_row = None
            for row in table.get_children():
                vals = table.item(row, "values")
                if str(vals[0]) == str(product["id"]):
                    staged_qty = int(vals[3])
                    existing_row = row
                    break

            if staged_qty + quantity > int(product["stock"]):
                messagebox.showwarning(
                    "Insufficient Stock",
                    f"Only {product['stock']} units available ({staged_qty} already in bill)."
                )
                return

            price = float(product["price"])
            if existing_row:
                new_qty = staged_qty + quantity
                new_total = new_qty * price
                table.item(existing_row, values=(product["id"], product["name"], f"{price:.2f}", new_qty, f"{new_total:.2f}"))
            else:
                line_total = quantity * price
                table.insert("", "end", values=(
                    product["id"], product["name"], f"{price:.2f}", quantity, f"{line_total:.2f}"
                ))

            recalculate_subtotal()
            qty.delete(0, "end")
            qty.insert(0, "1")

        except ValueError as error:
            messagebox.showerror("Invalid Quantity", str(error))

    def removeSelectedItem():
        selected_rows = table.selection()
        if not selected_rows:
            messagebox.showwarning("No Selection", "Select an item row from the bill table to remove.")
            return
        for row in selected_rows:
            table.delete(row)
        recalculate_subtotal()
        if table.get_children():
            getTotal()
        else:
            total.config(text="Total: ₹0.00")
            invoice.config(state="normal")
            invoice.delete("1.0", "end")
            invoice.config(state="disabled")

    def filter_products(event=None):
        query = search_var.get().strip().lower()
        all_prods = getproducts()
        if not query:
            dropdown.config(values=all_prods)
        else:
            filtered = [p for p in all_prods if query in p.lower()]
            dropdown.config(values=filtered)
            if filtered:
                dropdown.set(filtered[0])
            else:
                dropdown.set("No matching product")

    # Navigation Bar
    build_navbar(root, "New Bill", navbtn)

    # Main Container
    frame = tk.Frame(root, bg="#F0F2F5")
    frame.pack(fill="both", expand=True)

    frame.columnconfigure(0, weight=3, uniform="panels")
    frame.columnconfigure(1, weight=2, uniform="panels")
    frame.rowconfigure(0, weight=1)

    left_panel = tk.Frame(frame, bg="#F0F2F5")
    left_panel.grid(row=0, column=0, padx=(15, 8), pady=10, sticky="nsew")

    right_panel = tk.Frame(frame, bg="#F0F2F5")
    right_panel.grid(row=0, column=1, padx=(8, 15), pady=10, sticky="nsew")

    # =============================================
    # LEFT PANEL
    # =============================================
    customer_details = tk.LabelFrame(
        left_panel, text="Customer Details", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    customer_details.pack(fill="x", pady=(0, 10))
    customer_details.columnconfigure(1, weight=1)

    tk.Label(customer_details, text="Name:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    nameInput = tk.Entry(customer_details, font=("Segoe UI", 11), bg="#F8F9FA", relief="solid", bd=1)
    nameInput.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(customer_details, text="Phone:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    phoneInput = tk.Entry(customer_details, font=("Segoe UI", 11), bg="#F8F9FA", relief="solid", bd=1)
    phoneInput.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    # Add Item to Cart
    item_cart = tk.LabelFrame(
        left_panel, text="Add Item to Cart", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    item_cart.pack(fill="x", pady=5)
    item_cart.columnconfigure(1, weight=1)

    tk.Label(item_cart, text="Search:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=4, sticky="w")
    search_var = tk.StringVar()
    searchInput = tk.Entry(item_cart, textvariable=search_var, font=("Segoe UI", 11), bg="#F8F9FA", relief="solid", bd=1)
    searchInput.grid(row=0, column=1, padx=5, pady=4, sticky="ew")
    searchInput.bind("<KeyRelease>", filter_products)

    tk.Label(item_cart, text="Product:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    dropdown = ttk.Combobox(item_cart, values=getproducts(), state="readonly", font=("Segoe UI", 11))
    dropdown.set("Select product")
    dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(item_cart, text="Quantity:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    qty = tk.Spinbox(item_cart, from_=1, to=1000, font=("Segoe UI", 11), width=8)
    qty.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    add_item_btn = tk.Button(
        item_cart, text="Add to Bill", font=("Segoe UI", 11, "bold"),
        fg="white", bg="#1596FC", activebackground="#0F78CC", activeforeground="white",
        cursor="hand2", relief="flat", command=addItems
    )
    add_item_btn.grid(row=2, column=1, padx=5, pady=5, ipadx=10, ipady=2, sticky="e")

    # Current Bill Items Table
    bill_items = tk.LabelFrame(
        left_panel, text="Current Bill Items", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    bill_items.pack(fill="both", expand=True, pady=(5, 0))

    table_container = tk.Frame(bill_items, bg="#FFFFFF")
    table_container.pack(fill="both", expand=True)

    columns = ("ID", "Item Name", "Price", "Qty", "Total")
    table = ttk.Treeview(table_container, columns=columns, show="headings", height=6)
    for col in columns:
        table.heading(col, text=col)

    table.column("ID", width=60, anchor="w")
    table.column("Item Name", width=180, anchor="w")
    table.column("Price", width=80, anchor="e")
    table.column("Qty", width=50, anchor="center")
    table.column("Total", width=90, anchor="e")

    table_scroll = ttk.Scrollbar(table_container, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=table_scroll.set)
    table.pack(side="left", fill="both", expand=True)
    table_scroll.pack(side="right", fill="y")

    remove_btn = tk.Button(
        bill_items, text="Remove Selected Item", font=("Segoe UI", 10, "bold"),
        fg="white", bg="#E74C3C", activebackground="#C0392B", activeforeground="white",
        relief="flat", cursor="hand2", command=removeSelectedItem
    )
    remove_btn.pack(side="bottom", anchor="e", pady=(6, 0), ipadx=8, ipady=2)

    # =============================================
    # RIGHT PANEL
    # =============================================
    payment = tk.LabelFrame(
        right_panel, text="Payment & Calculation", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    payment.pack(fill="x", pady=(0, 10))
    payment.columnconfigure(1, weight=1)

    tk.Label(payment, text="Sub-Total:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=4, sticky="w")
    subamount = tk.Label(payment, text="₹0.00", font=("Segoe UI", 11, "bold"), bg="#FFFFFF")
    subamount.grid(row=0, column=1, padx=5, pady=4, sticky="e")

    tk.Label(payment, text="Discount (%):", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=1, column=0, padx=5, pady=4, sticky="w")
    discountInput = tk.Entry(payment, font=("Segoe UI", 11), width=10, justify="right")
    discountInput.insert(0, "0")
    discountInput.grid(row=1, column=1, padx=5, pady=4, sticky="e")

    tk.Label(payment, text="Tax / GST (%):", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=2, column=0, padx=5, pady=4, sticky="w")
    tax_gstInput = tk.Entry(payment, font=("Segoe UI", 11), width=10, justify="right")
    tax_gstInput.insert(0, "18")
    tax_gstInput.grid(row=2, column=1, padx=5, pady=4, sticky="e")

    ttk.Separator(payment, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=8)

    totalbtn = tk.Button(
        payment, text="Calculate Total", font=("Segoe UI", 10, "bold"),
        fg="white", bg="#27AE60", relief="flat", cursor="hand2", command=getTotal
    )
    totalbtn.grid(row=4, column=0, padx=5, pady=4, sticky="w")

    total = tk.Label(payment, text="Total: ₹0.00", font=("Segoe UI", 14, "bold"), fg="#27AE60", bg="#FFFFFF")
    total.grid(row=4, column=1, padx=5, pady=4, sticky="e")

    tk.Label(payment, text="Payment Method:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=5, column=0, padx=5, pady=4, sticky="w")
    methodInput = ttk.Combobox(payment, values=["Cash", "UPI", "Card"], state="readonly", font=("Segoe UI", 10), width=10)
    methodInput.set("UPI")
    methodInput.grid(row=5, column=1, padx=5, pady=4, sticky="e")

    # Invoice Preview
    invoice_frame = tk.LabelFrame(
        right_panel, text="Invoice Preview", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    invoice_frame.pack(fill="both", expand=True)

    invoice_content = tk.Frame(invoice_frame, bg="#FFFFFF")
    invoice_content.pack(fill="both", expand=True)

    invoice = tk.Text(invoice_content, font=("Consolas", 10), width=35, height=8, wrap="word", state="disabled")
    invoice_scroll = ttk.Scrollbar(invoice_content, orient="vertical", command=invoice.yview)
    invoice.configure(yscrollcommand=invoice_scroll.set)
    invoice.pack(side="left", fill="both", expand=True)
    invoice_scroll.pack(side="right", fill="y")

    # Actions
    button_frame = tk.Frame(invoice_frame, bg="#FFFFFF")
    button_frame.pack(side="bottom", fill="x", pady=(10, 0))

    def clear_invoice():
        nameInput.delete(0, "end")
        phoneInput.delete(0, "end")
        search_var.set("")
        for item in table.get_children():
            table.delete(item)
        dropdown.config(values=getproducts())
        dropdown.set("Select product")
        qty.delete(0, "end")
        qty.insert(0, "1")
        current_subtotal.set(0.0)
        subamount.config(text="₹0.00")
        total.config(text="Total: ₹0.00")
        discountInput.delete(0, "end")
        discountInput.insert(0, "0")
        tax_gstInput.delete(0, "end")
        tax_gstInput.insert(0, "18")
        methodInput.set("UPI")
        invoice.config(state="normal")
        invoice.delete("1.0", "end")
        invoice.config(state="disabled")

    def save_invoice():
        if not table.get_children():
            messagebox.showwarning("Empty Invoice", "Add items and calculate the total before saving.")
            return

        calc = getTotal()
        if calc is None:
            return
        subtotal_value, discount_percent, discount_amount, gst_percent, gst_amount, total_amount = calc

        itemlst = []
        stock_updates = {}
        for row_id in table.get_children():
            product_id, name, price, quantity, amount = table.item(row_id, "values")
            quantity = int(quantity)
            itemlst.append([product_id, quantity])
            stock_updates[product_id] = stock_updates.get(product_id, 0) + quantity

        for product_id, quantity in stock_updates.items():
            product = getproductdetails(product_id)
            if product is None or int(product["stock"]) < quantity:
                messagebox.showerror("Stock Error", f"Insufficient or unavailable stock for {product_id}.")
                return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Invoice",
            initialfile=f"Invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if not file_path:
            return

        saved_sale = saveHistory(
            itemlst,
            nameInput.get(),
            phoneInput.get(),
            subtotal_value,
            discount_percent,
            discount_amount,
            gst_percent,
            gst_amount,
            total_amount,
            methodInput.get()
        )
        if not saved_sale:
            return

        # Refresh invoice preview with real generated Invoice ID before writing file
        getInvoice(discount_amount, gst_amount, total_amount, saved_sale["invoice_id"])
        final_invoice_text = invoice.get("1.0", "end-1c")

        try:
            for product_id, quantity in stock_updates.items():
                if updateStock(product_id, quantity) is False:
                    raise RuntimeError(f"Stock update failed for {product_id}.")

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(final_invoice_text)

            dropdown.config(values=getproducts())
            messagebox.showinfo(
                "Sale Completed",
                f"Invoice {saved_sale['invoice_id']} saved, sales recorded, and inventory updated."
            )
            clear_invoice()

        except Exception as error:
            messagebox.showerror("Save Error", f"The sale could not be completed:\n{error}")

    clearbtn = tk.Button(
        button_frame, text="Clear", font=("Segoe UI", 10, "bold"),
        fg="#333333", bg="#E0E0E0", relief="flat", cursor="hand2", width=10, command=clear_invoice
    )
    clearbtn.pack(side="left")

    savebtn = tk.Button(
        button_frame, text="Complete & Save", font=("Segoe UI", 10, "bold"),
        fg="white", bg="#27AE60", relief="flat", cursor="hand2", command=save_invoice
    )
    savebtn.pack(side="right", ipadx=10, ipady=2)
