# database.py

import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INT AUTO_INCREMENT PRIMARY KEY,
            room_number VARCHAR(10),
            room_type VARCHAR(50),
            price FLOAT,
            status VARCHAR(20)
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(100),
            room_id INT,
            check_in DATE,
            check_out DATE,
            FOREIGN KEY (room_id) REFERENCES rooms(room_id)
        )
        """)
        self.conn.commit()

    def add_room(self, number, rtype, price):
        self.cursor.execute("INSERT INTO rooms (room_number, room_type, price, status) VALUES (%s, %s, %s, 'Available')",
                            (number, rtype, price))
        self.conn.commit()

    def view_rooms(self):
        self.cursor.execute("SELECT * FROM rooms")
        return self.cursor.fetchall()

    def update_room_status(self, room_id, status):
        self.cursor.execute("UPDATE rooms SET status = %s WHERE room_id = %s", (status, room_id))
        self.conn.commit()

    def delete_room(self, room_id):
        self.cursor.execute("DELETE FROM rooms WHERE room_id = %s", (room_id,))
        self.conn.commit()
        print("✅ Room deleted successfully.")

    def add_booking(self, customer_name, room_id, check_in, check_out):
        self.cursor.execute("INSERT INTO bookings (customer_name, room_id, check_in, check_out) VALUES (%s, %s, %s, %s)",
                            (customer_name, room_id, check_in, check_out))
        self.update_room_status(room_id, 'Booked')
        self.conn.commit()

    def view_bookings(self):
        self.cursor.execute("SELECT * FROM bookings")
        return self.cursor.fetchall()

    def delete_booking(self, booking_id):
        self.cursor.execute("SELECT room_id FROM bookings WHERE booking_id = %s", (booking_id,))
        room = self.cursor.fetchone()
        if room:
            room_id = room[0]
            self.cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
            self.update_room_status(room_id, 'Available')
            self.conn.commit()
            print("✅ Booking deleted and room set to Available.")
        else:
            print("❌ Booking not found.")
