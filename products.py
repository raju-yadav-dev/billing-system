import json
import os
from datetime import datetime
from tkinter import messagebox


PRODUCTS_FILE = "products.json"
SALES_FILE = "sales.json"


def load_all_products():
    if os.path.exists(PRODUCTS_FILE) and os.path.getsize(PRODUCTS_FILE) > 0:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
            items = json.load(file)
        if not isinstance(items, list):
            raise ValueError("Invalid products database structure")
        return items
    return []


def save_all_products(items):
    temp_file = "tempproduct.json"
    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(items, file, indent=4)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp_file, PRODUCTS_FILE)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def getproducts():
    try:
        items = load_all_products()
        products = []
        for item in items:
            products.append(
                f"{item['id']} - {item['name']} (₹{float(item['price']):.2f} | Stock: {item['stock']})"
            )
        return products
    except Exception as e:
        messagebox.showerror("Failed to get value", str(e))
        return []


def getproductdetails(item_id):
    try:
        products = load_all_products()
        for product in products:
            if product["id"] == item_id:
                return product
        return None
    except Exception as e:
        messagebox.showerror("Failed to get value", str(e))
        return None


def generate_next_product_id():
    items = load_all_products()
    max_num = 100
    for item in items:
        pid = str(item.get("id", ""))
        if pid.startswith("P") and pid[1:].isdigit():
            max_num = max(max_num, int(pid[1:]))
    return f"P{max_num + 1}"


def setproductdetails(*item):
    if len(item) < 4:
        messagebox.showerror("Product Error", "Product ID, Name, Price, and Stock are required.")
        return False

    product_id = str(item[0]).strip()
    name = str(item[1]).strip()
    price = float(item[2])
    stock = int(item[3])

    if not product_id or not name:
        messagebox.showerror("Product Error", "Product ID and Name cannot be empty.")
        return False
    if price < 0 or stock < 0:
        messagebox.showerror("Product Error", "Price and Stock cannot be negative.")
        return False

    try:
        products = load_all_products()
        for existing in products:
            if existing["id"].lower() == product_id.lower():
                messagebox.showerror("Product Error", f"Product ID '{product_id}' already exists.")
                return False

        product = {
            "id": product_id,
            "name": name,
            "price": price,
            "stock": stock
        }
        products.append(product)
        save_all_products(products)
        return True

    except Exception as e:
        messagebox.showerror("Product Error", str(e))
        return False


def editproductdetails(product_id, name, price, stock):
    try:
        products = load_all_products()
        for item in products:
            if item["id"] == product_id:
                item["name"] = str(name).strip()
                item["price"] = float(price)
                item["stock"] = int(stock)
                save_all_products(products)
                return True
        raise ValueError("Product ID not found.")
    except Exception as e:
        messagebox.showerror("Update Product Error", str(e))
        return False


def deleteproduct(product_id):
    try:
        products = load_all_products()
        updated = [item for item in products if item["id"] != product_id]
        if len(updated) == len(products):
            raise ValueError("Product ID not found.")
        save_all_products(updated)
        return True
    except Exception as e:
        messagebox.showerror("Delete Product Error", str(e))
        return False


def updateStock(productid, qty, add=False):
    try:
        items = load_all_products()
        for item in items:
            if item["id"] == productid:
                if add:
                    item["stock"] += int(qty)
                else:
                    if item["stock"] < int(qty):
                        raise ValueError("Insufficient stock available")
                    item["stock"] -= int(qty)

                save_all_products(items)
                return True

        raise ValueError("Product ID not found")

    except Exception as e:
        messagebox.showerror("Stock Update Failed", str(e))
        return False


def saveHistory(itemlst, nm, num, *pmnt):
    """Append one completed sale to sales.json."""
    if len(pmnt) != 7:
        messagebox.showerror(
            "Sales History Error",
            "Expected subtotal, discount %, discount amount, GST %, GST amount, total and payment method."
        )
        return False

    dt = datetime.now()
    sales = {
        "invoice_id": f"INV-{dt.strftime('%Y%m%d%H%M%S%f')}",
        "date": dt.strftime("%d-%m-%Y %H:%M"),
        "customer": {
            "name": nm.strip() if nm.strip() else "Walk-in Customer",
            "phone": num.strip() if num.strip() else "N/A"
        },
        "items": [],
        "subtotal": pmnt[0],
        "discount_percent": pmnt[1],
        "discount_amount": pmnt[2],
        "gst_percent": pmnt[3],
        "gst_amount": pmnt[4],
        "total": pmnt[5],
        "payment_method": pmnt[6]
    }

    temp_file = "sales_temp.json"

    try:
        for product_id, quantity in itemlst:
            product = getproductdetails(product_id)
            if product is None:
                raise ValueError(f"Product {product_id} was not found")

            sales["items"].append({
                "product_id": product_id,
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "amount": product["price"] * quantity
            })

        history = load_sales_history()
        history.append(sales)

        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temp_file, SALES_FILE)
        return sales

    except (OSError, ValueError, TypeError, KeyError) as error:
        messagebox.showerror("Sales History Error", str(error))
        return False

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def load_sales_history():
    if os.path.exists(SALES_FILE) and os.path.getsize(SALES_FILE) > 0:
        with open(SALES_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)
        if not isinstance(history, list):
            raise ValueError("Invalid sales database structure")
        return history
    return []
