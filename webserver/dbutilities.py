"""
Contains functions that are utilized by the main flask application
"""
import mariadb

def initialize_connection(dbuser, dbpassword, dbhost, dbport, dbname):
    """
    Initializes connection to database

    Returns:
        mariadb.connections.Connection: Object for interacting with the database
    """
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

