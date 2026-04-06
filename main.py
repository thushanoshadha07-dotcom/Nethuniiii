import sqlite3
from tkinter import *
from datetime import datetime

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS machines (id INTEGER PRIMARY KEY, name TEXT, rate REAL, status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS rentals (id INTEGER PRIMARY KEY, machine_id INTEGER, customer_id INTEGER, date TEXT, rate REAL)")

    conn.commit()
    conn.close()

# ---------- ADD MACHINE ----------
def add_machine():
    win = Toplevel(root)
    win.title("Add Machine")

    Label(win, text="Machine Name").pack()
    name = Entry(win)
    name.pack()

    Label(win, text="Monthly Rate").pack()
    rate = Entry(win)
    rate.pack()

    result = Label(win, text="")
    result.pack()

    def save():
        if not name.get() or not rate.get():
            result.config(text="Fill all fields", fg="red")
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO machines (name, rate, status) VALUES (?, ?, 'Available')",
                  (name.get(), rate.get()))
        conn.commit()
        conn.close()

        result.config(text="Machine Added Successfully", fg="green")

    Button(win, text="Save Machine", command=save).pack(pady=10)

# ---------- ADD CUSTOMER ----------
def add_customer():
    win = Toplevel(root)
    win.title("Add Customer")

    Label(win, text="Customer Name").pack()
    name = Entry(win)
    name.pack()

    Label(win, text="Phone").pack()
    phone = Entry(win)
    phone.pack()

    result = Label(win, text="")
    result.pack()

    def save():
        if not name.get() or not phone.get():
            result.config(text="Fill all fields", fg="red")
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO customers (name, phone) VALUES (?, ?)",
                  (name.get(), phone.get()))
        conn.commit()
        conn.close()

        result.config(text="Customer Added Successfully", fg="green")

    Button(win, text="Save Customer", command=save).pack(pady=10)

# ---------- NEW RENTAL ----------
def new_rental():
    win = Toplevel(root)
    win.title("New Rental")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    customers = c.execute("SELECT id FROM customers").fetchall()
    machines = c.execute("SELECT id FROM machines WHERE status='Available'").fetchall()
    conn.close()

    if not customers or not machines:
        Label(win, text="Add machine and customer first", fg="red").pack()
        return

    Label(win, text="Customer ID").pack()
    cust = StringVar(value=customers[0][0])
    OptionMenu(win, cust, *[c[0] for c in customers]).pack()

    Label(win, text="Machine ID").pack()
    mach = StringVar(value=machines[0][0])
    OptionMenu(win, mach, *[m[0] for m in machines]).pack()

    result = Label(win, text="")
    result.pack(pady=10)

    def save():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT rate FROM machines WHERE id=?", (mach.get(),))
        rate = c.fetchone()[0]

        c.execute(
            "INSERT INTO rentals (machine_id, customer_id, date, rate) VALUES (?, ?, ?, ?)",
            (mach.get(), cust.get(), datetime.now().strftime("%Y-%m-%d"), rate)
        )

        c.execute("UPDATE machines SET status='Rented' WHERE id=?", (mach.get(),))
        conn.commit()
        conn.close()

        result.config(text="RENTAL CREATED SUCCESSFULLY", fg="green")

    Button(win, text="Save Rental", command=save).pack(pady=10)

# ---------- VIEW RENTALS ----------
def view_rentals():
    win = Toplevel(root)
    win.title("All Rentals")
    win.geometry("600x300")

    listbox = Listbox(win, width=80)
    listbox.pack(fill=BOTH, expand=True)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    rentals = c.execute("SELECT * FROM rentals").fetchall()
    conn.close()

    for r in rentals:
        listbox.insert(END, f"{r[0]} | Machine {r[1]} | Customer {r[2]} | {r[3]} | Rs {r[4]}")

# ---------- RETURN MACHINE ----------
def return_machine():
    win = Toplevel(root)
    win.title("Return Machine")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    rented = c.execute("SELECT id FROM machines WHERE status='Rented'").fetchall()
    conn.close()

    if not rented:
        Label(win, text="No rented machines", fg="red").pack()
        return

    Label(win, text="Select Machine ID").pack()
    mach = StringVar(value=rented[0][0])
    OptionMenu(win, mach, *[m[0] for m in rented]).pack()

    result = Label(win, text="")
    result.pack(pady=10)

    def return_now():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("UPDATE machines SET status='Available' WHERE id=?", (mach.get(),))
        conn.commit()
        conn.close()

        result.config(text="MACHINE RETURNED SUCCESSFULLY", fg="green")

    Button(win, text="Return Machine", command=return_now).pack(pady=10)

# ---------- MONTHLY INCOME ----------
def monthly_income():
    win = Toplevel(root)
    win.title("Monthly Income")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT SUM(rate) FROM rentals")
    total = c.fetchone()[0]
    conn.close()

    if total is None:
        total = 0

    Label(win, text=f"TOTAL MONTHLY INCOME: Rs {total}",
          font=("Arial", 14), fg="green").pack(pady=30)

# ---------- LOGIN ----------
def login():
    if user.get() == "admin" and pwd.get() == "password":
        login_win.destroy()
        open_app()

# ---------- MAIN ----------
def open_app():
    global root
    root = Tk()
    root.title("Thushan Machine Center")

    Button(root, text="Add Machine", width=30, command=add_machine).pack(pady=2)
    Button(root, text="Add Customer", width=30, command=add_customer).pack(pady=2)
    Button(root, text="New Rental", width=30, command=new_rental).pack(pady=2)
    Button(root, text="View Rentals", width=30, command=view_rentals).pack(pady=2)
    Button(root, text="Return Machine", width=30, command=return_machine).pack(pady=2)
    Button(root, text="Monthly Income", width=30, command=monthly_income).pack(pady=2)

    root.mainloop()

# ---------- START ----------
init_db()

login_win = Tk()
login_win.title("Login")

Label(login_win, text="Username").pack()
user = Entry(login_win)
user.pack()

Label(login_win, text="Password").pack()
pwd = Entry(login_win, show="*")
pwd.pack()

Button(login_win, text="Login", command=login).pack(pady=10)

login_win.mainloop()
