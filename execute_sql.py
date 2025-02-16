import os
import mysql.connector
from mysql.connector import Error

# Fetch database credentials from GitHub Actions environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# SQL script file path
SQL_SCRIPT_PATH = "schema_changes.sql"

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
            print("Connected to MySQL database.")

            # Read and execute SQL script
            with open(SQL_SCRIPT_PATH, 'r') as file:
                sql_script = file.read()

            cursor = connection.cursor()
            for statement in sql_script.split(';'):
                if statement.strip():  # Skip empty statements
                    cursor.execute(statement)

            connection.commit()
            print("Database schema changes applied successfully.")

    except Error as e:
        print(f"Error while applying schema changes: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    execute_sql_script()
