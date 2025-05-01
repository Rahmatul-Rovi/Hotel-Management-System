import mysql.connector

# Connect to MySQL Workbench Database
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",  # <- change this
    database="hotel_db"               # <- change if needed
)

cursor = conn.cursor()

# Sample query: Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT
)
""")

print("Connected and table created!")

# Close connection
cursor.close()
conn.close()
