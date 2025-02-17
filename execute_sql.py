import os
import mysql.connector
from mysql.connector import Error

# Fetch database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# SQL script file path
SQL_SCRIPT_PATH = "schema_changes.sql"

def column_exists(cursor, table_name, column_name):
    """Check if a column exists in the table"""
    query = f"""
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = '{table_name}' AND COLUMN_NAME = '{column_name}'
    """
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] > 0

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

            cursor = connection.cursor()

            # Check if the 'budget' column exists in the 'projects' table
            if not column_exists(cursor, "projects", "budget"):
                print("✅ 'budget' column does not exist. Adding column.")
                cursor.execute("ALTER TABLE projects ADD COLUMN budget DECIMAL(10, 2)")
            
            # Read and execute the rest of the SQL script
            with open(SQL_SCRIPT_PATH, 'r') as file:
                sql_script = file.read()

            # Split the script into individual statements and execute each
            statements = sql_script.split(';')

            for statement in statements:
                if statement.strip():  # Skip empty statements
                    cursor.execute(statement)

                    # ✅ Fetch results for SELECT statements if any
                    if cursor.with_rows:
                        cursor.fetchall()  # Ensures no unread results

            # Commit the changes
            connection.commit()
            print("✅ Database schema changes applied successfully.")

    except Error as e:
        print(f"❌ Error while applying schema changes: {e}")
    finally:
        # Ensure cursor is closed properly
        if 'cursor' in locals() and cursor:
            cursor.close()

        # Ensure connection is closed properly
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    execute_sql_script()
