# students.py

import mysql.connector

def view_students():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="hotel_db"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    print("\n=== Student List ===")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
    
    cursor.close()
    conn.close()

view_students()
