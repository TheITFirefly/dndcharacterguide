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

    query = f"SELECT * FROM {table_name}" # Bad formatting is fine since this isn't user-submitted
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def is_user(username) -> bool:
    """
    Gets all usernames
    """
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

def delete_user(username):
    """
    Deletes a user from the database
    """
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "DELETE FROM Users WHERE username=%s"
    cursor.execute(query, (username,))

    conn.commit()
    conn.close()

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

def add_character(name, race_id, class_id, background_id, ability_scores, proficiency_bonus, username):
    """
    Adds a character to the database
    """
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "INSERT INTO Characters (CharacterName, RaceID, ClassID, BackgroundID, Strength_Ability_Score, Dexterity_Ability_Score, Constitution_Ability_Score, Intelligence_Ability_Score, Wisdom_Ability_Score, Charisma_Ability_Score, Proficiency_bonus, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(query, (name, race_id, class_id, background_id, ability_scores[0], ability_scores[1], ability_scores[2], ability_scores[3], ability_scores[4], ability_scores[5], proficiency_bonus, username))

    character_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return character_id

def add_saving_throw(character_id, name, modifier, proficiency):
    """
    Add a saving throw to a character
    """
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "INSERT INTO Saving_Throws (ID, Saving_ThrowName, Modifier, Proficiency) VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (character_id, name, modifier, proficiency))

    conn.commit()
    conn.close()

    return None

def add_skill(character_id, name, modifier, proficiency):
    """
    Add a skill to a character
    """
    conn = initialize_connection()
    cursor = conn.cursor()

    query = "INSERT INTO Skills (ID, SkillName, Modifier, Proficiency) VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (character_id, name, modifier, proficiency))

    conn.commit()
    conn.close()
    return None


def get_one_character(character_id):
    """
    Show character info for one single character.
    
    Args:
        character_id (int): unique character ID
    """
    conn = initialize_connection()
    cursor = conn.cursor()
    
    query = "SELECT CharacterName, RaceID, ClassID, BackgroundID FROM Characters WHERE ID = %s"
    cursor.execute(query, (character_id,))
    result = cursor.fetchall()
    conn.close()
    
    return result


def get_user_characters(username):
    """
    Show all characters linked to specific user ID

    Args:
        user_id (int): unique user ID
    """
    conn = initialize_connection()
    cursor = conn.cursor()
    
    query = "SELECT CharacterName, RaceID, ClassID, BackgroundID FROM Characters WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    conn.close()
    
    return result


def get_race_name(race_id):
    """
    Get the RaceName associated with race ID

    Args:
        race_id (int): unique Race ID
    """
    conn = initialize_connection()
    cursor = conn.cursor()
    
    query = "SELECT RaceName FROM Race WHERE ID = %s"
    cursor.execute(query, (race_id,))
    result = cursor.fetchall()
    conn.close()
    
    return result

def get_class_name(class_id):
    """
    Get the classname associated with race ID

    Args:
        class_id (int): unique class ID
    """
    conn = initialize_connection()
    cursor = conn.cursor()
    
    query = "SELECT ClassName FROM Class WHERE ClassID = %s"
    cursor.execute(query, (class_id,))
    result = cursor.fetchall()
    conn.close()
    
    return result

def get_background_name(background_id):
    """
    Get the background associated with race ID

    Args:
        background_id (int): unique background ID
    """
    conn = initialize_connection()
    cursor = conn.cursor()
    
    query = "SELECT BackgroundName FROM Background WHERE BackgroundID = %s"
    cursor.execute(query, (background_id,))
    result = cursor.fetchall()
    conn.close()
    
    return result