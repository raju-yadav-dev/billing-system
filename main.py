from screen import clear
import tkinter as tk
import auth


def btnclick(root, value):
    clear(root)
    if value == "signin":
        auth.signin(root)
    else:
        auth.signup(root)


def main():
    root = tk.Tk()
    root.title("Billing System")
    root.geometry("1280x720")
    root.configure(bg="#F0F2F5")

    frame = tk.Frame(root, bg="#F0F2F5")
    frame.pack(expand=True)

    msg1 = tk.Label(
        frame,
        text="Welcome to Billing Service",
        font=("Arial", 32, "bold"),
        bg="#F0F2F5",
        fg="#232E40"
    )
    msg1.grid(row=1, column=1, pady=10)

    msg2 = tk.Label(
        frame,
        text="A Digital way for fast work",
        font=("Arial", 24),
        fg="gray",
        bg="#F0F2F5"
    )
    msg2.grid(row=2, column=1, pady=10)

    btns = tk.Frame(frame, bg="#F0F2F5")
    btns.grid(row=3, column=1, pady=10)

    btn1 = tk.Button(
        btns,
        text="Lets Go",
        font=("Arial", 16),
        bg="#27ae60",
        fg="white",
        cursor="hand2",
        command=lambda: btnclick(root, "signin")
    )
    btn1.grid(row=1, column=1, pady=10, padx=5, ipadx=10)

    btn2 = tk.Button(
        btns,
        text="Create account",
        font=("Arial", 16),
        bg="#27ae60",
        fg="white",
        cursor="hand2",
        command=lambda: btnclick(root, "signup")
    )
    btn2.grid(row=1, column=2, pady=10, padx=5, ipadx=10)

    root.mainloop()


if __name__ == "__main__":
    main()
