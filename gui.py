import tkinter as tk
from tkinter import messagebox, ttk
from hotel import (
    add_room, view_rooms, add_booking, show_bookings,
    delete_room, delete_booking, calculate_booking_price
)

def add_room_gui():
    win = tk.Toplevel()
    win.title("Add Room")

    tk.Label(win, text="Room Number").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(win, text="Room Type").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(win, text="Price per Night").grid(row=2, column=0, padx=10, pady=5)

    entry_no = tk.Entry(win)
    entry_type = tk.Entry(win)
    entry_price = tk.Entry(win)

    entry_no.grid(row=0, column=1, padx=10, pady=5)
    entry_type.grid(row=1, column=1, padx=10, pady=5)
    entry_price.grid(row=2, column=1, padx=10, pady=5)

    def submit():
       try:
            room_no = entry_no.get()
            room_type = entry_type.get()
            price = float(entry_price.get())
            add_room(room_no, room_type, price)
            messagebox.showinfo("Success", "Room added successfully")
            win.destroy() 
       except ValueError:
         messagebox.showerror("Error", "Invalid price. Please enter a valid number.")


    tk.Button(win, text="Submit", bg="#4CAF50", fg="white", command=submit).grid(row=3, column=0, columnspan=2, pady=10)

def show_rooms_gui():
    win = tk.Toplevel()
    win.title("All Rooms")

    tree = ttk.Treeview(win, columns=("ID", "Room", "Type", "Price", "Available"), show="headings")
    tree.pack(fill="both", expand=True)

    for col in ("ID", "Room", "Type", "Price", "Available"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    rooms = view_rooms()
    if not rooms:  # If no rooms are available
        messagebox.showinfo("No Data", "No rooms found in the database.")
    else:
        for row in rooms:
            tree.insert("", "end", values=row)


def add_booking_gui():
    win = tk.Toplevel()
    win.title("Add Booking")

    labels = ["Customer Name", "Room ID", "Check-in (YYYY-MM-DD)", "Check-out (YYYY-MM-DD)"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(win, text=text).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(win)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    def submit():
        add_booking(entries[0].get(), int(entries[1].get()), entries[2].get(), entries[3].get())
        messagebox.showinfo("Success", "Booking added")
        win.destroy()

    tk.Button(win, text="Submit", bg="#FF9800", fg="white", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

def show_bookings_gui():
    win = tk.Toplevel()
    win.title("All Bookings")

    tree = ttk.Treeview(win, columns=("ID", "Room ID", "Customer", "Check-in", "Check-out"), show="headings")
    tree.pack(fill="both", expand=True)

    for col in ("ID", "Room ID", "Customer", "Check-in", "Check-out"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    for row in show_bookings():
        tree.insert("", "end", values=row)


def delete_room_gui():
    win = tk.Toplevel()
    win.title("Delete Room")

    tk.Label(win, text="Enter Room ID to delete:").pack(padx=10, pady=5)
    entry = tk.Entry(win)
    entry.pack(padx=10, pady=5)

    def delete():
        delete_room(int(entry.get()))
        messagebox.showinfo("Deleted", "Room deleted successfully.")
        win.destroy()

    tk.Button(win, text="Delete", bg="#F44336", fg="white", command=delete).pack(pady=10)

def delete_booking_gui():
    win = tk.Toplevel()
    win.title("Delete Booking")

    tk.Label(win, text="Enter Booking ID to delete:").pack(padx=10, pady=5)
    entry = tk.Entry(win)
    entry.pack(padx=10, pady=5)

    def delete():
        delete_booking(int(entry.get()))
        messagebox.showinfo("Deleted", "Booking deleted successfully.")
        win.destroy()

    tk.Button(win, text="Delete", bg="#D32F2F", fg="white", command=delete).pack(pady=10)

def calculate_price_gui():
    win = tk.Toplevel()
    win.title("Calculate Booking Price")

    labels = ["Room ID", "Check-in Date (YYYY-MM-DD)", "Check-out Date (YYYY-MM-DD)"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(win, text=text).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(win)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    result_label = tk.Label(win, text="", font=("Arial", 12), fg="green")
    result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def calculate():
        try:
            room_id = int(entries[0].get())
            check_in = entries[1].get()
            check_out = entries[2].get()
            price = calculate_booking_price(room_id, check_in, check_out)
            result_label.config(text=f"Total Price: ₹ {price:.2f}")
        except Exception as e:
            result_label.config(text=f"Error: {e}", fg="red")

    tk.Button(win, text="Calculate", bg="#795548", fg="white", command=calculate).grid(row=3, column=0, columnspan=2, pady=10)


# ========== Main Window ==========
root = tk.Tk()
root.title("Hotel Management System")
root.geometry("400x600")
root.configure(bg="#e3f2fd")

tk.Label(root, text="HOTEL MANAGEMENT SYSTEM", font=("Helvetica", 16, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=20)

btn_style = {
    "width": 25,
    "padx": 5,
    "pady": 5,
    "font": ("Helvetica", 11),
}

tk.Button(root, text="Add Room", command=add_room_gui, bg="#388E3C", fg="white", **btn_style).pack(pady=5)
tk.Button(root, text="View Rooms", command=show_rooms_gui, bg="#1976D2", fg="white", **btn_style).pack(pady=5)
tk.Button(root, text="Add Booking", command=add_booking_gui, bg="#F57C00", fg="white", **btn_style).pack(pady=5)
tk.Button(root, text="Show Bookings", command=show_bookings_gui, bg="#7B1FA2", fg="white", **btn_style).pack(pady=5)
tk.Button(root, text="Delete Room", command=delete_room_gui, bg="#C62828", fg="white", **btn_style).pack(pady=5)
tk.Button(root, text="Delete Booking", command=delete_booking_gui, bg="#B71C1C", fg="white", **btn_style).pack(pady=5)
tk.Button(root, text="Calculate Booking Price", command=calculate_price_gui, bg="#5D4037", fg="white", **btn_style).pack(pady=5)

tk.Button(root, text="Exit", command=root.destroy, bg="gray", fg="white", **btn_style).pack(pady=20)

root.mainloop()
