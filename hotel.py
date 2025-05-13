import customtkinter as ctk
import mysql.connector
from datetime import datetime

# ---------- MySQL Connection ----------
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="hotel_db"
    )

# ---------- Database Functions ----------
def add_customer(name, age):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cursor.close()
    conn.close()
    return "✅ Customer added successfully!"

def view_customers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return "\n".join([f"ID: {r[0]}, Name: {r[1]}, Age: {r[2]}" for r in rows]) or "No customers found."

def add_room(room_number, room_type, price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rooms (room_number, room_type, price_per_night, is_available)
        VALUES (%s, %s, %s, TRUE)
    """, (room_number, room_type, price))
    conn.commit()
    cursor.close()
    conn.close()
    return "✅ Room added successfully!"

def view_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return "\n".join([f"ID: {r[0]}, Room: {r[1]}, Type: {r[2]}, Price: {r[3]}, Available: {r[4]}" for r in rows]) or "No rooms found."

def show_available_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms WHERE is_available = TRUE")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return "\n".join([f"Room No: {r[1]}, Type: {r[2]}, Price: {r[3]}" for r in rows]) or "No available rooms."

def add_booking(customer_name, room_id, check_in, check_out):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (customer_name, room_id, check_in, check_out)
        VALUES (%s, %s, %s, %s)
    """, (customer_name, room_id, check_in, check_out))
    cursor.execute("UPDATE rooms SET is_available = FALSE WHERE id = %s", (room_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return "✅ Booking added successfully."

def show_bookings():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, r.room_number, b.customer_name, b.check_in, b.check_out
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return "\n".join([
        f"Booking ID: {r[0]}, Room: {r[1]}, Customer: {r[2]}, From: {r[3]}, To: {r[4]}"
        for r in rows]) or "No bookings found."

def calculate_booking_price(room_id, check_in, check_out):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT price_per_night FROM rooms WHERE id = %s", (room_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if not result:
        return "❌ Room not found."

    price = result[0]
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    nights = (check_out_date - check_in_date).days

    if nights <= 0:
        return "❌ Invalid date range."

    total = nights * price
    return f"🧾 Total for {nights} nights: {total} BDT"

def delete_room(room_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return "✅ Room deleted successfully."

def delete_booking(booking_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT room_id FROM bookings WHERE id = %s", (booking_id,))
    room = cursor.fetchone()
    if room:
        room_id = room[0]
        cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        cursor.execute("UPDATE rooms SET is_available = TRUE WHERE id = %s", (room_id,))
        conn.commit()
        result = "✅ Booking deleted and room marked available."
    else:
        result = "❌ Booking not found."
    cursor.close()
    conn.close()
    return result

# ---------- GUI ----------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("1000x900")
app.title("🏨 Hotel Management System")

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True)

button_frame = ctk.CTkFrame(main_frame)
button_frame.pack(pady=20)

entry_frame = ctk.CTkFrame(main_frame)
entry_frame.pack(pady=10)
entry_frame.pack_forget()

output_box = ctk.CTkTextbox(main_frame, height=200, width=500)
output_box.pack(side="bottom", fill="both", padx=20, pady=10)
output_box.configure(wrap="word")
output_box.pack_forget()

close_btn = ctk.CTkButton(main_frame, text="❌ Close", command=lambda: show_main_menu(), width=80)
close_btn.place_forget()

# Button definitions
buttons_data = [
    ("➕ Add Customer", lambda: show_form("add_customer", ["Name", "Age"])),
    ("👁️ View Customers", lambda: show_result(view_customers())),
    ("🏠 Add Room", lambda: show_form("add_room", ["Room Number", "Room Type", "Price"])),
    ("📋 View Rooms", lambda: show_result(view_rooms())),
    ("✅ Available Rooms", lambda: show_result(show_available_rooms())),
    ("📅 Add Booking", lambda: show_form("add_booking", ["Customer Name", "Room ID", "Check-In", "Check-Out"])),
    ("🔍 View Bookings", lambda: show_result(show_bookings())),
    ("💵 Calculate Price", lambda: show_form("calculate_price", ["Room ID", "Check-In", "Check-Out"])),
    ("❌ Delete Room", lambda: show_form("delete_room", ["Room ID"])),
    ("🗑️ Delete Booking", lambda: show_form("delete_booking", ["Booking ID"]))
]

buttons = []
for text, cmd in buttons_data:
    btn = ctk.CTkButton(button_frame, text=text, command=cmd, width=250)
    btn.pack(pady=5)
    buttons.append(btn)

def show_main_menu():
    entry_frame.pack_forget()
    output_box.pack_forget()
    close_btn.place_forget()
    for b in buttons:
        b.pack(pady=5)

def show_form(action, fields):
    for b in buttons:
        b.pack_forget()
    for widget in entry_frame.winfo_children():
        widget.destroy()

    entries = []
    for field in fields:
        lbl = ctk.CTkLabel(entry_frame, text=field)
        lbl.pack(pady=2)
        ent = ctk.CTkEntry(entry_frame, width=300)
        ent.pack(pady=2)
        entries.append(ent)

    def submit():
        values = [e.get() for e in entries]
        if action == "add_customer":
            show_result(add_customer(values[0], int(values[1])))
        elif action == "add_room":
            show_result(add_room(values[0], values[1], float(values[2])))
        elif action == "add_booking":
            show_result(add_booking(values[0], int(values[1]), values[2], values[3]))
        elif action == "calculate_price":
            show_result(calculate_booking_price(int(values[0]), values[1], values[2]))
        elif action == "delete_room":
            show_result(delete_room(int(values[0])))
        elif action == "delete_booking":
            show_result(delete_booking(int(values[0])))

    ctk.CTkButton(entry_frame, text="Submit", command=submit).pack(pady=10)
    entry_frame.pack()
    close_btn.place(relx=0.9, rely=0.05)

def show_result(result):
    entry_frame.pack_forget()
    output_box.pack()
    output_box.delete("1.0", "end")
    output_box.insert("end", result)
    close_btn.place(relx=0.9, rely=0.05)

# Run the app
app.mainloop()
