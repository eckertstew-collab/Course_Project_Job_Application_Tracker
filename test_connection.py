
import mysql.connector

from database import get_db

try:
    conn = get_db()

    if conn.is_connected():
        print("Successfully connected to MySQL!")
        print("Database: job_tracker")

    conn.close()

except mysql.connector.Error as err:
    print("Database connection failed:", err)
