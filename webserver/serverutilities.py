"""
Contains only functions that don't interact with the database
"""
from bcrypt import hashpw, gensalt, checkpw
from flask import session
def hash_password(password) -> str:
    """
    Hashes a given password

    Returns:
        str: hashed password
    """
    return hashpw(password.encode('utf-8'), gensalt())

def correct_password(hashed_password, entered_password) -> bool:
    """
    Returns whether the entered password matches the hashed password
    """
    return checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8'))

def user_authenticated():
    """
    Check whether user is authenticated
    Returns:
        Tuple (session, authenticated)
    """
    if 'authenticated' in session:
        if session['authenticated']:
            return True
    session['authenticated'] = False
    return False

def calculate_modifier(score):
    """
    Calculates modifier to be put into database from user score input during character creation
    Does not take into account proficiency
    """
    modifier = (score - 10) // 2
    return modifier
