"""
This module takes in json objects and uses them to populate the setup database with its static data
"""
import sys
import os
import json
from dotenv import load_dotenv
import mariadb

# Database connection variables
load_dotenv()
dbuser = os.getenv('dbuser')
dbpassword = os.getenv('dbpassword')
dbhost = os.getenv('dbhost')
dbport = os.getenv('dbport')
dbname = os.getenv('dbname')

SCRIPT_PATH = __file__

def initialize_connection():
    """
    Initializes connection to database

    Returns:
        mariadb.connections.Connection: Object for interacting with the database
    """
    print("Attempting to connect to database...")
    try:
        connection = mariadb.connect(
            user=dbuser,
            password=dbpassword,
            host=dbhost,
            port=int(dbport),
            database=dbname
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    print('connection created successfully')
    return connection

def main():
    """
    Main function for module

    Returns:
        int: 0 for success, error codes if any
    """
    conn = initialize_connection()
    cursor = conn.cursor()

    cursor.execute("show tables;")
    query_results = cursor.fetchall()

    table_names = []
    for item in query_results:
        table_names.append(item[0])

    data_path = os.path.dirname(SCRIPT_PATH)
    data_path = os.path.dirname(data_path)
    data_path = os.path.join(data_path, 'data', 'initial-data.json')
    with open(data_path, encoding="utf-8") as file:
        loaded_json = json.load(file)

    for table_name, json_object in loaded_json.items():
        for name, page_number in json_object.items():
            sql_insert = f"insert into {table_name} ({table_name}Name, Page_Number) values('{name}', {page_number});"
            print(sql_insert)
            cursor.execute(sql_insert)
            conn.commit()

    conn.close()

if __name__ == "__main__":
    main()
