from products import load_sales_history
from tkinter import ttk, filedialog, messagebox
from screen import indian_format, build_navbar
from home import navbtn
from datetime import datetime, timedelta
import tkinter as tk


def salesHistory(root):
    root.title("Retail Billing & Inventory System - Sales History")
    root.geometry("1280x720")
    root.configure(bg="#F0F2F5")

    build_navbar(root, "Sales History", navbtn)

    frame = tk.Frame(root, bg="#F0F2F5")
    frame.pack(fill="both", expand=True)

    frame.columnconfigure(0, weight=3, uniform="sales_panels")
    frame.columnconfigure(1, weight=2, uniform="sales_panels")
    frame.rowconfigure(0, weight=1)

    left_panel = tk.Frame(frame, bg="#F0F2F5")
    left_panel.grid(row=0, column=0, padx=(15, 8), pady=10, sticky="nsew")

    right_panel = tk.Frame(frame, bg="#F0F2F5")
    right_panel.grid(row=0, column=1, padx=(8, 15), pady=10, sticky="nsew")

    # =============================================
    # LEFT PANEL: Filter, Summary & Sales Table
    # =============================================
    filter_frame = tk.LabelFrame(
        left_panel, text="Search & Report Filters", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    filter_frame.pack(fill="x", pady=(0, 10))

    tk.Label(filter_frame, text="Search:", font=("Segoe UI", 11), bg="#FFFFFF").pack(side="left", padx=(0, 6))
    search_var = tk.StringVar()
    search_entry = tk.Entry(filter_frame, textvariable=search_var, font=("Segoe UI", 11), bg="#F8F9FA", relief="solid", bd=1, width=22)
    search_entry.pack(side="left", padx=(0, 12))

    tk.Label(filter_frame, text="Period:", font=("Segoe UI", 11), bg="#FFFFFF").pack(side="left", padx=(0, 6))
    period_combo = ttk.Combobox(
        filter_frame,
        values=["All Time", "Today", "Last 7 Days", "This Month"],
        state="readonly",
        font=("Segoe UI", 10),
        width=13
    )
    period_combo.set("All Time")
    period_combo.pack(side="left", padx=(0, 10))

    summary_lbl = tk.Label(
        filter_frame, text="Bills: 0 | Total: ₹0.00",
        font=("Segoe UI", 11, "bold"), fg="#27AE60", bg="#FFFFFF"
    )
    summary_lbl.pack(side="right")

    history_frame = tk.LabelFrame(
        left_panel, text="Transaction Records", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    history_frame.pack(fill="both", expand=True)

    table_wrap = tk.Frame(history_frame, bg="#FFFFFF")
    table_wrap.pack(fill="both", expand=True)

    columns = ("Invoice ID", "Date", "Customer", "Phone", "Payment", "Total (₹)")
    tree = ttk.Treeview(table_wrap, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)

    tree.column("Invoice ID", width=165, anchor="w")
    tree.column("Date", width=115, anchor="center")
    tree.column("Customer", width=120, anchor="w")
    tree.column("Phone", width=95, anchor="center")
    tree.column("Payment", width=70, anchor="center")
    tree.column("Total (₹)", width=95, anchor="e")

    scroll = ttk.Scrollbar(table_wrap, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    # =============================================
    # RIGHT PANEL: Invoice Details & Reprint/Export
    # =============================================
    detail_frame = tk.LabelFrame(
        right_panel, text="Invoice Details", font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF", fg="#232E40", padx=10, pady=10
    )
    detail_frame.pack(fill="both", expand=True)

    text_wrap = tk.Frame(detail_frame, bg="#FFFFFF")
    text_wrap.pack(fill="both", expand=True)

    detail_text = tk.Text(text_wrap, font=("Consolas", 10), wrap="word", state="disabled")
    detail_scroll = ttk.Scrollbar(text_wrap, orient="vertical", command=detail_text.yview)
    detail_text.configure(yscrollcommand=detail_scroll.set)
    detail_text.pack(side="left", fill="both", expand=True)
    detail_scroll.pack(side="right", fill="y")

    btn_frame = tk.Frame(detail_frame, bg="#FFFFFF")
    btn_frame.pack(side="bottom", fill="x", pady=(10, 0))

    sales_cache = {}

    def format_sale_receipt(sale):
        cust = sale.get("customer", {})
        receipt = f"""========================================
         RETAIL BILLING INVOICE
========================================
Invoice No : {sale.get('invoice_id', '')}
Date       : {sale.get('date', '')}
Customer   : {cust.get('name', '')}
Phone      : {cust.get('phone', '')}
----------------------------------------
Item                  Qty      Amount
----------------------------------------
"""
        for item in sale.get("items", []):
            receipt += (
                f"{str(item.get('name', ''))[:20]:<20} x{str(item.get('quantity', 0)):<4} "
                f"₹{indian_format(item.get('amount', 0)):>9}\n"
            )

        receipt += f"""----------------------------------------
Subtotal:                ₹{indian_format(sale.get('subtotal', 0)):>10}
Discount ({sale.get('discount_percent', 0)}%):        -₹{indian_format(sale.get('discount_amount', 0)):>10}
Tax / GST ({sale.get('gst_percent', 0)}%):       +₹{indian_format(sale.get('gst_amount', 0)):>10}
----------------------------------------
TOTAL:                   ₹{indian_format(sale.get('total', 0)):>10}
Payment Method: {sale.get('payment_method', '')}
========================================
        THANK YOU FOR SHOPPING!
========================================"""
        return receipt

    def on_select_sale(event):
        selected = tree.selection()
        if not selected:
            return
        inv_id = tree.item(selected[0], "values")[0]
        sale = sales_cache.get(inv_id)
        if not sale:
            return
        detail_text.config(state="normal")
        detail_text.delete("1.0", "end")
        detail_text.insert("1.0", format_sale_receipt(sale))
        detail_text.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", on_select_sale)

    def matches_period(date_str, period):
        if period == "All Time":
            return True
        try:
            sale_dt = datetime.strptime(date_str[:10], "%d-%m-%Y")
        except ValueError:
            return True
        now = datetime.now()
        if period == "Today":
            return sale_dt.date() == now.date()
        if period == "Last 7 Days":
            return sale_dt.date() >= (now - timedelta(days=7)).date()
        if period == "This Month":
            return sale_dt.year == now.year and sale_dt.month == now.month
        return True

    def refresh_sales(event=None):
        for item in tree.get_children():
            tree.delete(item)
        sales_cache.clear()

        query = search_var.get().strip().lower()
        period = period_combo.get()
        all_sales = load_sales_history()

        filtered_total = 0.0
        count = 0

        for sale in reversed(all_sales):
            inv_id = sale.get("invoice_id", "")
            date_str = sale.get("date", "")
            cust_name = sale.get("customer", {}).get("name", "")
            cust_phone = sale.get("customer", {}).get("phone", "")
            pay_method = sale.get("payment_method", "")
            tot = float(sale.get("total", 0))

            if not matches_period(date_str, period):
                continue
            if query and (
                query not in inv_id.lower()
                and query not in cust_name.lower()
                and query not in cust_phone.lower()
            ):
                continue

            sales_cache[inv_id] = sale
            tree.insert("", "end", values=(
                inv_id, date_str, cust_name, cust_phone, pay_method, indian_format(tot)
            ))
            filtered_total += tot
            count += 1

        summary_lbl.config(text=f"Bills: {count} | Total: ₹{indian_format(filtered_total)}")

    def export_selected_invoice():
        content = detail_text.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showwarning("No Invoice Selected", "Select an invoice from the table to export.")
            return
        selected = tree.selection()
        inv_id = tree.item(selected[0], "values")[0] if selected else "Invoice"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Download Invoice",
            initialfile=f"{inv_id}.txt"
        )
        if not file_path:
            return
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Exported", "Invoice saved successfully.")

    tk.Button(
        btn_frame, text="Download / Export Invoice", font=("Segoe UI", 10, "bold"),
        bg="#27AE60", fg="white", relief="flat", cursor="hand2", command=export_selected_invoice
    ).pack(side="right", ipadx=10, ipady=3)

    search_entry.bind("<KeyRelease>", refresh_sales)
    period_combo.bind("<<ComboboxSelected>>", refresh_sales)
    refresh_sales()
