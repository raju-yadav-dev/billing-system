# Retail Billing & Inventory Management System

A desktop Billing and Inventory Management application built with **Python** and **Tkinter**, using local **JSON** files for persistent data storage. Designed to automate invoice generation, tax/discount calculations, inventory tracking, and sales reporting.

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Data Files & Demo Credentials](#data-files--demo-credentials)
- [Prerequisites & How to Run](#prerequisites--how-to-run)

---

## Overview
Many small and medium businesses still rely on manual billing or spreadsheets, which often results in calculation mistakes, slow checkout times, inaccurate stock tracking, and difficulty retrieving past invoices. This application centralizes product management, billing calculations, receipt generation, and transaction history in a clean desktop interface.

---

## Key Features
1. **User Authentication (`auth.py`, `database.py`)**
   - Secure Sign In and Sign Up screens with masked password fields (`*`), duplicate username checks, and email validation.
2. **Home Dashboard (`home.py`)**
   - Displays real-time business metrics: **Total Products**, **Low Stock Alerts ($\le 10$ units)**, **Today's Sales**, and **Total Revenue**.
   - Quick-action shortcuts, recent invoice history, and a low-stock watchlist.
3. **Automated Billing & Invoice Generation (`home.py`)**
   - Live product search and dropdown selection with real-time stock validation.
   - Add or remove items in the cart with automatic subtotal calculation.
   - Configurable **Discount (%)** and **Tax / GST (%)** calculations formatted in Indian currency style (`₹1,23,456.00`).
   - Support for multiple payment methods (**Cash**, **UPI**, **Card**).
   - Live receipt preview, `.txt` invoice export, automatic stock deduction, and transaction logging.
4. **Product & Stock Management (`stock.py`, `products.py`)**
   - Search inventory by product ID or name.
   - Add new products (with auto-suggested IDs like `P111`), edit prices/stock quantities, delete products, and perform quick stock refills.
5. **Sales History & Reporting (`sales.py`)**
   - Filter past transactions by **All Time**, **Today**, **Last 7 Days**, or **This Month**.
   - Search invoices by Invoice ID, customer name, or phone number.
   - Inspect full itemized receipts and download/export past invoices as `.txt` files.

---

## Workflow
```text
Login / Sign Up → Dashboard → New Bill → Enter Customer Details → Search & Add Products → Enter Quantity → Apply Discount & GST → Select Payment Method → Complete & Save → Auto-Update Stock & Record Sale
```

---

## Project Structure
```text
Billing System/
├── main.py           # Application entry point and welcome screen
├── auth.py           # Sign In and Sign Up user interface
├── database.py       # User account validation and storage (userdata.json)
├── screen.py         # Shared UI helpers (clear screen, Indian currency format, navbar)
├── home.py           # Home dashboard and main New Bill / POS screen
├── stock.py          # Product & Inventory management and quick restock screen
├── sales.py          # Sales History, period filters, and invoice export screen
├── products.py       # JSON read/write operations for products and sales
├── products.json     # Product catalog and current stock levels
├── sales.json        # Completed sales transactions and invoice records
├── userdata.json     # Registered user accounts  
└── README.md         # Project documentation
```

---

## Data Files & Demo Credentials
* **Default Login Credentials:**
  * **Username:** `admin`
  * **Password:** `admin@123`
* **JSON Storage:** All updates to users, products, stock quantities, and sales history are saved atomically using temporary files (`os.replace`) to prevent data corruption.

---

## Prerequisites & How to Run
1. **Python Version:** Python 3.8 or higher (uses built-in `tkinter`, `json`, `os`, and `datetime` libraries—no external `pip` packages required).
2. **Launch the Application:**
   ```bash
   cd "Billing System"
   python main.py
   ```