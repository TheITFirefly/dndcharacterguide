"""
This runs the flask webserver that users will interact with

Returns:
    None?
"""
import os
from flask import Flask, session, render_template, request, redirect, url_for, flash
from dbutilities import initialize_connection, get_table_contents
from dotenv import load_dotenv

# Load environment variables from .env file to get secret
load_dotenv()

# Initialize the flask app
app = Flask(__name__)
app.secret_key = os.getenv("secret")

@app.route("/")
def home_page():
    """
    Contains buttons to sign up and login if unauthenticated
    Redirects to /characters if authenticated already
    """
    return

@app.route("/login")
def login():
    """
    Contains form to log in. Flask documentation has good example with session
    """
    return

@app.route("/logout")
def logout():
    """
    Hit with a POST request to logout
    """
    return

@app.route("/signup")
def signup_page():
    """
    Contains form to create an account
    """
    return

@app.route("/create-account")
def create_account():
    """
    Hit with PUT? request to create account if it doesn't exist already
    """
    return

@app.route("/account")
def account_page():
    """
    Page containing buttons to either delete account or change password
    """
    return

@app.route("/account/delete-account/<str:username>")
def delete_account():
    """
    Hit with DELETE request to delete account
    """
    return

@app.route("/account/change-password")
def change_password():
    """
    Hit with PUT? request to change password
    """
    return

@app.route("/party")
def party_page():
    """
    Page containing buttons to join a party or create a party
    """
    return

@app.route("/party/create")
def create_party():
    """
    Page containing form to create party
    """
    return

@app.route("/party/join")
def join_party():
    """
    Page containing available parties to join
    """
    return

@app.route("/characters")
def character_page():
    """
    Page containing characters in a grid
    Shows the following for each character
        - name
        - race
        - class
        - background
    Also contains buttons to view/edit/delete each character
    """
    return

@app.route("/characters/show/<int:character_id>")
def get_character_details():
    """
    Page to show details for a particular character
    """
    return

@app.route("/characters/create")
def create_character():
    """
    Page to create a new character
    """
    return

@app.route("/characters/edit/<int:character_id>")
def edit_character_details():
    """
    Page to edit details for a particular character
    """
    return

@app.route("/characters/delete/<int:character_id>")
def delete_character():
    """
    Hit with a DELETE request to delete a character
    """
    return

if __name__ == "__main__":
    app.run(port=8080, debug=True) # TODO: Students PLEASE remove debug=True when put in production
