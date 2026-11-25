from tkinter import messagebox
import os
import json


USER_FILE = "userdata.json"


def _read_users():
    if os.path.exists(USER_FILE) and os.path.getsize(USER_FILE) > 0:
        with open(USER_FILE, "r", encoding="utf-8") as file:
            users = json.load(file)
        if not isinstance(users, list):
            raise ValueError("Invalid user database structure")
        return users
    return []


def _write_users(users):
    temp_file = "temp_users.json"
    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp_file, USER_FILE)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def addUser(*val):
    if len(val) < 5:
        messagebox.showerror("SignUp Error", "All fields are required.")
        return False

    name = val[0].strip()
    username = val[1].strip()
    mail_id = val[2].strip()
    password = val[3]
    confirm_password = val[4]

    if not name or not username or not mail_id or not password:
        messagebox.showerror("SignUp Error", "Please fill in all fields.")
        return False

    if "@" not in mail_id or "." not in mail_id:
        messagebox.showerror("SignUp Error", "Please enter a valid Mail ID.")
        return False

    if password != confirm_password:
        messagebox.showerror("SignUp Error", "Password and Confirm Password do not match.")
        return False

    try:
        users = _read_users()

        for existing in users:
            if existing.get("Username", "").lower() == username.lower():
                messagebox.showerror("SignUp Error", "Username already exists.")
                return False

        user = {
            "Name": name,
            "Username": username,
            "Mail-ID": mail_id,
            "Password": password
        }
        users.append(user)
        _write_users(users)
        return True

    except Exception as e:
        messagebox.showerror("SignUp Error", str(e))
        return False


def checkUser(*val):
    if len(val) < 2:
        return False

    username = val[0].strip()
    password = val[1]

    if not username or not password:
        return False

    try:
        users = _read_users()
        for user in users:
            if user.get("Username") == username and user.get("Password") == password:
                return True
        return False

    except FileNotFoundError:
        return False

    except Exception as e:
        messagebox.showerror("Retrieval Error", str(e))
        return False
