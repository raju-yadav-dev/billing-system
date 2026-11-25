import tkinter as tk


def clear(root):
    for widget in root.winfo_children():
        widget.destroy()


def indian_format(number):
    num = f"{float(number):.2f}"
    integer, decimal = num.split(".")

    sign = ""
    if integer.startswith("-"):
        sign = "-"
        integer = integer[1:]

    if len(integer) > 3:
        last_three = integer[-3:]
        remaining = integer[:-3]
        remaining = ",".join(
            [remaining[max(i - 2, 0):i] for i in range(len(remaining), 0, -2)][::-1]
        )
        integer = remaining + "," + last_three

    return sign + integer + "." + decimal


def build_navbar(root, active_page, nav_callback):
    nav = tk.Frame(root, bg="#232E40", height=70)
    nav.pack(side="top", fill="x")
    nav.pack_propagate(False)

    nav_title = tk.Label(
        nav,
        text="BILLING & INVENTORY SYSTEM",
        font=("Segoe UI", 18, "bold"),
        fg="white",
        bg="#232E40"
    )
    nav_title.pack(side="left", padx=20, pady=15)

    btnval = ["Logout", "Sales History", "Product & Stock", "New Bill", "Home"]
    for val in btnval:
        is_active = (val.lower() == active_page.lower())
        bg_color = "#1596FC" if is_active else ("#C0392B" if val == "Logout" else "#333F57")
        hover_color = "#0F78CC" if is_active else ("#96281B" if val == "Logout" else "#42506B")

        b = tk.Button(
            nav,
            text=val,
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg=bg_color,
            activebackground=hover_color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda v=val: nav_callback(root, v)
        )
        b.pack(
            side="right",
            padx=(5, 20 if val == "Logout" else 5),
            pady=15,
            ipadx=10,
            ipady=4
        )
