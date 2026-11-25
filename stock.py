from products import (
    load_all_products,
    setproductdetails,
    editproductdetails,
    deleteproduct,
    updateStock,
    generate_next_product_id
)
from tkinter import ttk, messagebox
from screen import indian_format, build_navbar
from home import navbtn
import tkinter as tk


def productStock(root):
    root.title("Retail Billing & Inventory System - Product & Stock")
    root.geometry("1280x720")
    root.configure(bg="#F0F2F5")

    build_navbar(root, "Product & Stock", navbtn)

    frame = tk.Frame(root, bg="#F0F2F5")
    frame.pack(fill="both", expand=True)

    frame.columnconfigure(0, weight=3, uniform="stock_panels")
    frame.columnconfigure(1, weight=2, uniform="stock_panels")
    frame.rowconfigure(0, weight=1)

    left_panel = tk.Frame(frame, bg="#F0F2F5")
    left_panel.grid(row=0, column=0, padx=(15, 8), pady=10, sticky="nsew")

    right_panel = tk.Frame(frame, bg="#F0F2F5")
    right_panel.grid(row=0, column=1, padx=(8, 15), pady=10, sticky="nsew")

    # =============================================
    # LEFT PANEL: Inventory List & Search
    # =============================================
    inv_frame = tk.LabelFrame(
        left_panel, text="Product Inventory", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    inv_frame.pack(fill="both", expand=True)

    search_bar = tk.Frame(inv_frame, bg="#FFFFFF")
    search_bar.pack(fill="x", pady=(0, 8))

    tk.Label(search_bar, text="Search Product:", font=("Segoe UI", 11), bg="#FFFFFF").pack(side="left", padx=(0, 8))
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_bar, textvariable=search_var, font=("Segoe UI", 11), bg="#F8F9FA", relief="solid", bd=1)
    search_entry.pack(side="left", fill="x", expand=True)

    table_wrap = tk.Frame(inv_frame, bg="#FFFFFF")
    table_wrap.pack(fill="both", expand=True)

    columns = ("ID", "Product Name", "Price (₹)", "Stock", "Status")
    tree = ttk.Treeview(table_wrap, columns=columns, show="headings", height=16)
    for col in columns:
        tree.heading(col, text=col)

    tree.column("ID", width=75, anchor="center")
    tree.column("Product Name", width=230, anchor="w")
    tree.column("Price (₹)", width=110, anchor="e")
    tree.column("Stock", width=80, anchor="center")
    tree.column("Status", width=110, anchor="center")

    scroll = ttk.Scrollbar(table_wrap, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    def refresh_table(query=""):
        for item in tree.get_children():
            tree.delete(item)
        q = query.strip().lower()
        for p in load_all_products():
            if q and q not in p["id"].lower() and q not in p["name"].lower():
                continue
            stk = int(p["stock"])
            status = "Out of Stock" if stk == 0 else ("Low Stock" if stk <= 10 else "In Stock")
            tree.insert("", "end", values=(
                p["id"],
                p["name"],
                indian_format(p["price"]),
                stk,
                status
            ))

    search_entry.bind("<KeyRelease>", lambda e: refresh_table(search_var.get()))

    # =============================================
    # RIGHT PANEL: Add / Edit Product & Quick Restock
    # =============================================
    form_frame = tk.LabelFrame(
        right_panel, text="Add / Update Product", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=12, pady=12
    )
    form_frame.pack(fill="x", pady=(0, 10))
    form_frame.columnconfigure(1, weight=1)

    tk.Label(form_frame, text="Product ID:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=6, sticky="w")
    id_entry = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#F8F9FA", relief="solid", bd=1)
    id_entry.insert(0, generate_next_product_id())
    id_entry.grid(row=0, column=1, padx=5, pady=6, sticky="ew")

    tk.Label(form_frame, text="Product Name:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=1, column=0, padx=5, pady=6, sticky="w")
    name_entry = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#F8F9FA", relief="solid", bd=1)
    name_entry.grid(row=1, column=1, padx=5, pady=6, sticky="ew")

    tk.Label(form_frame, text="Price (₹):", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=2, column=0, padx=5, pady=6, sticky="w")
    price_entry = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#F8F9FA", relief="solid", bd=1)
    price_entry.grid(row=2, column=1, padx=5, pady=6, sticky="ew")

    tk.Label(form_frame, text="Stock Qty:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=3, column=0, padx=5, pady=6, sticky="w")
    stock_entry = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#F8F9FA", relief="solid", bd=1)
    stock_entry.grid(row=3, column=1, padx=5, pady=6, sticky="ew")

    def clear_form():
        id_entry.config(state="normal")
        id_entry.delete(0, "end")
        id_entry.insert(0, generate_next_product_id())
        name_entry.delete(0, "end")
        price_entry.delete(0, "end")
        stock_entry.delete(0, "end")
        tree.selection_remove(tree.selection())

    def on_row_select(event):
        selected = tree.selection()
        if not selected:
            return
        vals = tree.item(selected[0], "values")
        id_entry.config(state="normal")
        id_entry.delete(0, "end")
        id_entry.insert(0, vals[0])
        id_entry.config(state="readonly")

        name_entry.delete(0, "end")
        name_entry.insert(0, vals[1])

        price_entry.delete(0, "end")
        price_entry.insert(0, str(vals[2]).replace(",", ""))

        stock_entry.delete(0, "end")
        stock_entry.insert(0, vals[3])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    def handle_add():
        try:
            pid = id_entry.get().strip()
            pname = name_entry.get().strip()
            price = float(price_entry.get())
            stk = int(stock_entry.get())
            if setproductdetails(pid, pname, price, stk):
                messagebox.showinfo("Added", f"Product '{pname}' added successfully.")
                clear_form()
                refresh_table(search_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for Price and Stock.")

    def handle_update():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a product from the table first to update.")
            return
        try:
            pid = id_entry.get().strip()
            pname = name_entry.get().strip()
            price = float(price_entry.get())
            stk = int(stock_entry.get())
            if not pname:
                messagebox.showerror("Invalid Input", "Product Name cannot be empty.")
                return
            if price < 0 or stk < 0:
                messagebox.showerror("Invalid Input", "Price and Stock cannot be negative.")
                return
            if editproductdetails(pid, pname, price, stk):
                messagebox.showinfo("Updated", f"Product '{pid}' updated successfully.")
                clear_form()
                refresh_table(search_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for Price and Stock.")

    def handle_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a product from the table to delete.")
            return
        pid = tree.item(selected[0], "values")[0]
        pname = tree.item(selected[0], "values")[1]
        if messagebox.askyesno("Confirm Delete", f"Delete '{pname}' ({pid}) from inventory?"):
            if deleteproduct(pid):
                messagebox.showinfo("Deleted", "Product removed from inventory.")
                clear_form()
                refresh_table(search_var.get())

    btn_row = tk.Frame(form_frame, bg="#FFFFFF")
    btn_row.grid(row=4, column=0, columnspan=2, pady=(12, 4), sticky="ew")

    tk.Button(
        btn_row, text="Add New", font=("Segoe UI", 10, "bold"),
        bg="#27AE60", fg="white", relief="flat", cursor="hand2", command=handle_add
    ).pack(side="left", padx=(0, 6), ipadx=10, ipady=4)

    tk.Button(
        btn_row, text="Update Selected", font=("Segoe UI", 10, "bold"),
        bg="#1596FC", fg="white", relief="flat", cursor="hand2", command=handle_update
    ).pack(side="left", padx=6, ipadx=10, ipady=4)

    tk.Button(
        btn_row, text="Delete", font=("Segoe UI", 10, "bold"),
        bg="#E74C3C", fg="white", relief="flat", cursor="hand2", command=handle_delete
    ).pack(side="left", padx=6, ipadx=10, ipady=4)

    tk.Button(
        btn_row, text="Reset", font=("Segoe UI", 10, "bold"),
        bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=clear_form
    ).pack(side="right", ipadx=10, ipady=4)

    # Quick Restock Card
    restock_frame = tk.LabelFrame(
        right_panel, text="Quick Stock Refill", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=12, pady=12
    )
    restock_frame.pack(fill="x", pady=5)
    restock_frame.columnconfigure(1, weight=1)

    tk.Label(restock_frame, text="Add Quantity:", font=("Segoe UI", 11), bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=6, sticky="w")
    restock_spin = tk.Spinbox(restock_frame, from_=1, to=5000, font=("Segoe UI", 11), width=10)
    restock_spin.grid(row=0, column=1, padx=5, pady=6, sticky="w")

    def handle_restock():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a product in the inventory table to add stock.")
            return
        try:
            add_qty = int(restock_spin.get())
            if add_qty <= 0:
                raise ValueError("Quantity must be greater than zero.")
            pid = tree.item(selected[0], "values")[0]
            if updateStock(pid, add_qty, add=True):
                messagebox.showinfo("Stock Updated", f"Added {add_qty} units to {pid}.")
                clear_form()
                refresh_table(search_var.get())
        except ValueError as e:
            messagebox.showerror("Invalid Quantity", str(e))

    tk.Button(
        restock_frame, text="Add Stock", font=("Segoe UI", 10, "bold"),
        bg="#27AE60", fg="white", relief="flat", cursor="hand2", command=handle_restock
    ).grid(row=0, column=1, padx=5, pady=6, ipadx=12, ipady=3, sticky="e")

    refresh_table()
