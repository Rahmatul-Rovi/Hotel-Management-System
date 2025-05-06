# hotel_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector

# Database connection setup
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="hotel_db"
    )

# Hotel Management System GUI Class
class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("800x600")

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        self.customer_tab = ttk.Frame(notebook)
        self.room_tab = ttk.Frame(notebook)
        self.booking_tab = ttk.Frame(notebook)

        notebook.add(self.customer_tab, text='Customers')
        notebook.add(self.room_tab, text='Rooms')
        notebook.add(self.booking_tab, text='Bookings')

        self.create_customer_tab()
        self.create_room_tab()
        self.create_booking_tab()

    # CUSTOMER TAB
    def create_customer_tab(self):
        tk.Label(self.customer_tab, text="Name").grid(row=0, column=0)
        tk.Label(self.customer_tab, text="Age").grid(row=1, column=0)

        self.customer_name = tk.Entry(self.customer_tab)
        self.customer_age = tk.Entry(self.customer_tab)

        self.customer_name.grid(row=0, column=1)
        self.customer_age.grid(row=1, column=1)

        tk.Button(self.customer_tab, text="Add Customer", command=self.add_customer).grid(row=2, column=0, columnspan=2)
        tk.Button(self.customer_tab, text="View Customers", command=self.view_customers).grid(row=3, column=0, columnspan=2)

        self.customer_list = tk.Text(self.customer_tab, height=10, width=60)
        self.customer_list.grid(row=4, column=0, columnspan=2, pady=10)

    def add_customer(self):
        name = self.customer_name.get()
        age = self.customer_age.get()
        if not name or not age:
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (name, age))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Customer added")
            self.customer_name.delete(0, tk.END)
            self.customer_age.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def view_customers(self):
        self.customer_list.delete(1.0, tk.END)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            for row in rows:
                self.customer_list.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}\n")
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # ROOM TAB
    def create_room_tab(self):
        tk.Label(self.room_tab, text="Room Number").grid(row=0, column=0)
        tk.Label(self.room_tab, text="Room Type").grid(row=1, column=0)
        tk.Label(self.room_tab, text="Price/Night").grid(row=2, column=0)

        self.room_number = tk.Entry(self.room_tab)
        self.room_type = tk.Entry(self.room_tab)
        self.room_price = tk.Entry(self.room_tab)

        self.room_number.grid(row=0, column=1)
        self.room_type.grid(row=1, column=1)
        self.room_price.grid(row=2, column=1)

        tk.Button(self.room_tab, text="Add Room", command=self.add_room).grid(row=3, column=0, columnspan=2)
        tk.Button(self.room_tab, text="View Rooms", command=self.view_rooms).grid(row=4, column=0, columnspan=2)

        self.room_list = tk.Text(self.room_tab, height=10, width=60)
        self.room_list.grid(row=5, column=0, columnspan=2, pady=10)

    def add_room(self):
        room_number = self.room_number.get()
        room_type = self.room_type.get()
        price = self.room_price.get()
        if not room_number or not room_type or not price:
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO rooms (room_number, room_type, price_per_night, is_available) VALUES (%s, %s, %s, TRUE)",
                           (room_number, room_type, price))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Room added")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def view_rooms(self):
        self.room_list.delete(1.0, tk.END)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rooms")
            rows = cursor.fetchall()
            for row in rows:
                self.room_list.insert(tk.END, f"ID: {row[0]}, No: {row[1]}, Type: {row[2]}, Price: {row[3]}, Available: {row[4]}\n")
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # BOOKING TAB
    def create_booking_tab(self):
        tk.Label(self.booking_tab, text="Customer Name").grid(row=0, column=0)
        tk.Label(self.booking_tab, text="Room ID").grid(row=1, column=0)
        tk.Label(self.booking_tab, text="Check-in (YYYY-MM-DD)").grid(row=2, column=0)
        tk.Label(self.booking_tab, text="Check-out (YYYY-MM-DD)").grid(row=3, column=0)

        self.booking_name = tk.Entry(self.booking_tab)
        self.booking_room_id = tk.Entry(self.booking_tab)
        self.booking_checkin = tk.Entry(self.booking_tab)
        self.booking_checkout = tk.Entry(self.booking_tab)

        self.booking_name.grid(row=0, column=1)
        self.booking_room_id.grid(row=1, column=1)
        self.booking_checkin.grid(row=2, column=1)
        self.booking_checkout.grid(row=3, column=1)

        tk.Button(self.booking_tab, text="Add Booking", command=self.add_booking).grid(row=4, column=0, columnspan=2)
        tk.Button(self.booking_tab, text="View Bookings", command=self.view_bookings).grid(row=5, column=0, columnspan=2)

        self.booking_list = tk.Text(self.booking_tab, height=10, width=60)
        self.booking_list.grid(row=6, column=0, columnspan=2, pady=10)

    def add_booking(self):
        name = self.booking_name.get()
        room_id = self.booking_room_id.get()
        check_in = self.booking_checkin.get()
        check_out = self.booking_checkout.get()
        try:
            datetime.strptime(check_in, "%Y-%m-%d")
            datetime.strptime(check_out, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Use YYYY-MM-DD format")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bookings (customer_name, room_id, check_in, check_out)
                VALUES (%s, %s, %s, %s)
            """, (name, room_id, check_in, check_out))
            cursor.execute("UPDATE rooms SET is_available = FALSE WHERE id = %s", (room_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Booking added")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def view_bookings(self):
        self.booking_list.delete(1.0, tk.END)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.id, r.room_number, b.customer_name, b.check_in, b.check_out
                FROM bookings b
                JOIN rooms r ON b.room_id = r.id
            """)
            rows = cursor.fetchall()
            for row in rows:
                self.booking_list.insert(tk.END, f"Booking ID: {row[0]}, Room: {row[1]}, Name: {row[2]}, From: {row[3]}, To: {row[4]}\n")
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

# MAIN PROGRAM
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()
