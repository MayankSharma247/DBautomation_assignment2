import os
import mysql.connector
from mysql.connector import Error
 
# Fetch database credentials from GitHub Actions environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
 
def execute_sql_script(sql_file):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        with open(sql_file, "r") as file:
            sql_commands = file.read().split(";")
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)
        connection.commit()
        print("SQL script executed successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
 
if __name__ == "__main__":
    execute_sql_script("schema_changes.sql")
