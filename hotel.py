import mysql.connector
from datetime import datetime
#from database import Database  # Make sure database.py exists with a class Database

def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="hotel_db"
    )

def add_customer(name, age):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO students (name, age) VALUES (%s, %s)"
    cursor.execute(query, (name, age))
    conn.commit()
    print("Customer added successfully!")
    cursor.close()
    conn.close()

def view_customers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    print("\n=== Customer List ===")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
    cursor.close()
    conn.close()

def add_room(room_number, room_type, price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rooms (room_number, room_type, price_per_night, is_available)
        VALUES (%s, %s, %s, TRUE)
    """, (room_number, room_type, price))
    conn.commit()
    print("Room added successfully.")
    cursor.close()
    conn.close()

def view_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    rows = cursor.fetchall()
    print("\n=== Room List ===")
    for row in rows:
        print(f"ID: {row[0]}, Room: {row[1]}, Type: {row[2]}, Price: {row[3]}, Available: {row[4]}")
    cursor.close()
    conn.close()

def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="hotel_db"
    )

def update_room_status(room_id, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE rooms SET is_available = %s WHERE id = %s", (status == "Available", room_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_room(room_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
    conn.commit()
    print("✅ Room deleted successfully.")
    cursor.close()
    conn.close()

def delete_booking(booking_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT room_id FROM bookings WHERE id = %s", (booking_id,))
    room = cursor.fetchone()
    
    if room:
        room_id = room[0]
        cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        conn.commit()
        print("✅ Booking deleted.")
        cursor.close()
        conn.close()
        update_room_status(room_id, 'Available')
        print("✅ Room set to Available.")
    else:
        print("❌ Booking not found.")
        cursor.close()
        conn.close()

def show_available_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms WHERE is_available = TRUE")
    rows = cursor.fetchall()
    print("\n=== Available Rooms ===")
    for row in rows:
        print(f"Room No: {row[1]}, Type: {row[2]}, Price: {row[3]}")
    cursor.close()
    conn.close()

def add_booking(customer_name, room_id, check_in, check_out):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (customer_name, room_id, check_in, check_out)
        VALUES (%s, %s, %s, %s)
    """, (customer_name, room_id, check_in, check_out))
    cursor.execute("UPDATE rooms SET is_available = FALSE WHERE id = %s", (room_id,))
    conn.commit()
    print("Booking added successfully.")
    cursor.close()
    conn.close()

def show_bookings():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, r.room_number, b.customer_name, b.check_in, b.check_out
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
    """)
    rows = cursor.fetchall()
    print("\n=== Bookings ===")
    for row in rows:
        print(f"Booking ID: {row[0]}, Room: {row[1]}, Customer: {row[2]}, From: {row[3]}, To: {row[4]}")
    cursor.close()
    conn.close()

def calculate_booking_price(room_id, check_in, check_out):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT price_per_night FROM rooms WHERE id = %s", (room_id,))
    result = cursor.fetchone()
    
    if not result:
        print("Room not found.")
        return

    price = result[0]
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    nights = (check_out_date - check_in_date).days

    if nights <= 0:
        print("Invalid date range.")
        return

    total = nights * price
    print(f"\nTotal for {nights} nights: {total} BDT")
    cursor.close()
    conn.close()

def main():
  # Assuming Database class has delete_room and delete_booking methods

    while True:
        print("\n========= Hotel Management =========")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Add Room")
        print("4. View Rooms")
        print("5. Show Available Rooms")
        print("6. Add Booking")
        print("7. Show Bookings")
        print("8. Calculate Booking Price")
        print("9. Delete Room")
        print("10. Delete Booking")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter customer name: ")
            age = int(input("Enter customer age: "))
            add_customer(name, age)
        elif choice == "2":
            view_customers()
        elif choice == "3":
            r_no = input("Enter room number: ")
            r_type = input("Enter room type: ")
            price = float(input("Enter price per night: "))
            add_room(r_no, r_type, price)
        elif choice == "4":
            view_rooms()
        elif choice == "5":
            show_available_rooms()
        elif choice == "6":
            customer = input("Customer name: ")
            room_id = int(input("Room ID: "))
            check_in = input("Check-in (YYYY-MM-DD): ")
            check_out = input("Check-out (YYYY-MM-DD): ")
            add_booking(customer, room_id, check_in, check_out)
        elif choice == "7":
            show_bookings()
        elif choice == "8":
            room_id = int(input("Room ID: "))
            check_in = input("Check-in (YYYY-MM-DD): ")
            check_out = input("Check-out (YYYY-MM-DD): ")
            calculate_booking_price(room_id, check_in, check_out)
        elif choice == "9":
            room_id = int(input("Enter Room ID to delete: "))
            delete_room(room_id)
        elif choice == "10":
            booking_id = int(input("Enter Booking ID to delete: "))
            delete_booking(booking_id)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
