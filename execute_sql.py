import os
import mysql.connector
from mysql.connector import Error

# Fetch database credentials from GitHub Actions environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# SQL script file path
SQL_SCRIPT_PATH = "departments.sql"

def execute_sql_script():
    """Executes the SQL script file to apply schema changes."""
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            print("✅ Connected to MySQL database.")

            # Read and execute SQL script
            with open(SQL_SCRIPT_PATH, 'r') as file:
                sql_script = file.read()

            cursor = connection.cursor()

            # Execute each SQL statement separately
            for statement in sql_script.split(';'):
                if statement.strip():  # Skip empty statements
                    cursor.execute(statement)

                    # ✅ Fix: Fetch results if a SELECT statement is executed
                    if cursor.with_rows:
                        cursor.fetchall()  # Ensures no unread results

            connection.commit()
            print("✅ Database schema changes applied successfully.")

    except Error as e:
        print(f"❌ Error while applying schema changes: {e}")
    finally:
        # ✅ Ensure cursor is closed properly
        if 'cursor' in locals() and cursor:
            cursor.close()

        # ✅ Ensure connection is closed properly
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    execute_sql_script()
