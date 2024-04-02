"""
Contains only functions that interact with the database
"""
import os
import mariadb
from dotenv import load_dotenv

def initialize_connection():
    """
    Initializes connection to database

    Returns:
        mariadb.connections.Connection: Object for interacting with the database
    """
    load_dotenv()
    dbuser = os.getenv('dbuser')
    dbpassword = os.getenv('dbpassword')
    dbhost = os.getenv('dbhost')
    dbport = os.getenv('dbport')
    dbname = os.getenv('dbname')
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
    return connection

def get_table_contents(table_name):
    """
    Gets contents of a particular table

    Returns:
        Result of query
    """
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM %s"
    cursor.execute(query, (table_name,))
    result = cursor.fetchall()
    conn.close()
    return result

def is_user(username) -> bool:
    """
    Gets all usernames
    """
    print("Fetching username")
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "SELECT username from Users WHERE username = %s;"
    cursor.execute(query, (username,))
    print(cursor.rowcount > 0)
    if cursor.rowcount > 0:
        conn.close()
        return True
    conn.close()
    return False

def create_user(username, hashed_password):
    """
    Adds a user to the Users table if they don't already exist
    """
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "INSERT INTO Users (username, password) VALUES (%s, %s);"
    cursor.execute(query, (username, hashed_password))

    conn.commit()
    rowcount = cursor.rowcount
    conn.close()

    return rowcount > 0

def add_totp(username, seed):
    """
    Adds TOTP to a user's account
    Adds ability to reset password
    """
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "UPDATE Users SET totpseed = %s WHERE username = %s;"
    cursor.execute(query, (seed,username,))
    conn.commit()
    conn.close()
    return

def get_totp_seed(username) -> str:
    """
    Gets the stored TOTP seed for a user.
    """
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "SELECT totpseed FROM Users WHERE username = %s;"
    cursor.execute(query, (username,))
    result = cursor.fetchall()

    conn.close()

    if result:
        return result[0][0]
    else:
        return None

def totp_enabled(username):
    """
    Determine if a user has TOTP enabled

    Returns:
        Bool: whether or not user has TOTP enabled
    """
    # Initialize connection to database
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "SELECT * from Users WHERE username = %s AND totpseed IS NOT NULL"
    cursor.execute(query, (username,))
    rowcount = cursor.rowcount
    # Close connection to database when done to prevent hanging
    conn.close()
    #
    return rowcount == 1

def get_password_hash(username) -> str:
    """
    Gets the stored password hash for a user.
    """
    print("Getting password")
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "SELECT password FROM Users WHERE username = %s;"
    cursor.execute(query, (username,))
    result = cursor.fetchall()

    conn.close()

    if result:
        return result[0][0]
    else:
        return None

def change_password_hash(username, new_hash):
    """
    Alter the user table with new password hash
    Returns whether password was successfully changed or not
    """
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "UPDATE Users SET password = %s WHERE username = %s;"
    cursor.execute(query, (new_hash, username,))
    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False
