"""
Contains only functions that don't interact with the database
"""
from bcrypt import hashpw, gensalt, checkpw
from flask import session
def hash_password(password) -> str:
    """
    Hashes a password given
    """
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    return hashed_password

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
