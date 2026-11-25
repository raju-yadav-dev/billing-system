from database import addUser, checkUser
from screen import clear
from home import home
import tkinter as tk
from tkinter import messagebox


def signin(root):
    fnt = ("Arial", 24)
    root.title("SignIn Page")
    root.geometry("1280x720")
    root.configure(bg="#F0F2F5")

    frame = tk.Frame(
        root,
        borderwidth=5,
        relief="groove",
        bg="#FFFFFF"
    )
    frame.pack(expand=True)

    lbl = tk.Label(frame, text="SignIn Page", font=("Arial", 26, "bold"), bg="#FFFFFF", fg="#232E40")
    lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

    usnmlabel = tk.Label(frame, text="Username", font=fnt, bg="#FFFFFF")
    usnmlabel.grid(row=1, column=0, padx=(50, 10), pady=(40, 20), sticky="w")
    usnminput = tk.Entry(frame, font=fnt)
    usnminput.grid(row=1, column=1, padx=(10, 50), pady=(40, 20))
    usnminput.focus_set()

    passlabel = tk.Label(frame, text="Password", font=fnt, bg="#FFFFFF")
    passlabel.grid(row=2, column=0, padx=(50, 10), pady=20, sticky="w")
    passinput = tk.Entry(frame, font=fnt, show="*")
    passinput.grid(row=2, column=1, padx=(10, 50), pady=20)

    btns = tk.Frame(frame, bg="#FFFFFF")
    btns.grid(row=3, column=0, columnspan=2, pady=20)

    btn1 = tk.Button(
        btns,
        text="SignIn",
        font=("Arial", 16),
        bg="#27ae60",
        fg="white",
        cursor="hand2",
        command=lambda: btnclick(root, "verify", usnminput.get(), passinput.get())
    )
    btn1.grid(row=0, column=0, pady=10, padx=10, ipadx=15)

    btn2 = tk.Button(
        btns,
        text="Don't have account",
        font=("Arial", 16),
        bg="#27ae60",
        fg="white",
        cursor="hand2",
        command=lambda: btnclick(root, "signup")
    )
    btn2.grid(row=0, column=1, pady=10, padx=10, ipadx=10)

    root.bind("<Return>", lambda event: btnclick(root, "verify", usnminput.get(), passinput.get()))


def signup(root):
    fnt = ("Arial", 22)
    root.title("SignUp Page")
    root.geometry("1280x720")
    root.configure(bg="#F0F2F5")

    frame = tk.Frame(
        root,
        borderwidth=5,
        relief="groove",
        bg="#FFFFFF"
    )
    frame.pack(expand=True)

    lbl = tk.Label(frame, text="Create Account", font=("Arial", 26, "bold"), bg="#FFFFFF", fg="#232E40")
    lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=(25, 10))

    namelabel = tk.Label(frame, text="Full Name", font=fnt, bg="#FFFFFF")
    namelabel.grid(row=1, column=0, padx=(50, 10), pady=(20, 15), sticky="w")
    nameinput = tk.Entry(frame, font=fnt)
    nameinput.grid(row=1, column=1, padx=(10, 50), pady=(20, 15))
    nameinput.focus_set()

    usnmlabel = tk.Label(frame, text="Username", font=fnt, bg="#FFFFFF")
    usnmlabel.grid(row=2, column=0, padx=(50, 10), pady=15, sticky="w")
    usnminput = tk.Entry(frame, font=fnt)
    usnminput.grid(row=2, column=1, padx=(10, 50), pady=15)

    maillabel = tk.Label(frame, text="Mail ID", font=fnt, bg="#FFFFFF")
    maillabel.grid(row=3, column=0, padx=(50, 10), pady=15, sticky="w")
    mailinput = tk.Entry(frame, font=fnt)
    mailinput.grid(row=3, column=1, padx=(10, 50), pady=15)

    passlabel = tk.Label(frame, text="New Password", font=fnt, bg="#FFFFFF")
    passlabel.grid(row=4, column=0, padx=(50, 10), pady=15, sticky="w")
    passinput = tk.Entry(frame, font=fnt, show="*")
    passinput.grid(row=4, column=1, padx=(10, 50), pady=15)

    cfpslabel = tk.Label(frame, text="Confirm Password", font=fnt, bg="#FFFFFF")
    cfpslabel.grid(row=5, column=0, padx=(50, 10), pady=15, sticky="w")
    cfpsinput = tk.Entry(frame, font=fnt, show="*")
    cfpsinput.grid(row=5, column=1, padx=(10, 50), pady=15)

    btns = tk.Frame(frame, bg="#FFFFFF")
    btns.grid(row=6, column=0, columnspan=2, pady=20)

    btn1 = tk.Button(
        btns,
        text="SignUp",
        font=("Arial", 16),
        bg="#27ae60",
        fg="white",
        cursor="hand2",
        command=lambda: btnclick(
            root,
            "enroll",
            nameinput.get(),
            usnminput.get(),
            mailinput.get(),
            passinput.get(),
            cfpsinput.get()
        )
    )
    btn1.grid(row=0, column=0, pady=10, padx=10, ipadx=15)

    btn2 = tk.Button(
        btns,
        text="Already have account",
        font=("Arial", 16),
        bg="#27ae60",
        fg="white",
        cursor="hand2",
        command=lambda: btnclick(root, "signin")
    )
    btn2.grid(row=0, column=1, pady=10, padx=10, ipadx=10)


def btnclick(root, val, *value):
    root.unbind("<Return>")
    if val == "signin":
        clear(root)
        signin(root)

    elif val == "signup":
        clear(root)
        signup(root)

    elif val == "verify":
        res = checkUser(*value)
        if res:
            messagebox.showinfo("Success", "User verified successfully")
            clear(root)
            home(root)
        else:
            messagebox.showerror("Failed", "Invalid Username or Password")
            clear(root)
            signin(root)

    elif val == "enroll":
        success = addUser(*value)
        if success:
            messagebox.showinfo("Success", "User added successfully")
            clear(root)
            signin(root)
