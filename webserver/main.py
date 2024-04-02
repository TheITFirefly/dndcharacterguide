"""
This runs the flask webserver that users will interact with

Returns:
    None?
"""
import os
import pyotp
import time
from flask import Flask, session, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_qrcode import QRcode
from dbutilities import is_user, get_password_hash, change_password_hash, create_user, totp_enabled, add_totp, get_totp_seed
from serverutilities import hash_password, correct_password, user_authenticated
from dotenv import load_dotenv

# Load environment variables from .env file to get secret
load_dotenv()

# Initialize the flask app
app = Flask(__name__)
app.secret_key = os.getenv("secret")
QRcode(app)

@app.route("/")
def index():
    """
    Page containing buttons to sign up or log in
    """
    if user_authenticated():
        return redirect(url_for('characters'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Contains form to log in if unauthenticated.
    Redirects to viewing characters if authenticated
    """
    authenticated = user_authenticated()
    if authenticated:
        return redirect(url_for('characters'))
    if request.method == 'POST':
        username = request.form['username']
        entered_password = request.form['password']
        if is_user(username):
            if correct_password(get_password_hash(username), entered_password):
                session['authenticated'] = True
                session['username'] = username
                return redirect(url_for('verify_totp'))
            error = "Entered password was wrong"
            return render_template('login.html', error=error)
        error = "Username not found"
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Logs the user out if they are logged in
    """
    session['authenticated'] = False
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/verify-totp', methods=['GET', 'POST'])
def verify_totp():
    """
    Return user to login page if wrong totp code
    """
    if totp_enabled(session['username']):
        session['authenticated'] = False
        render_template('verify-totp.html')
    else:
        redirect(url_for('characters'))
    if request.method == 'POST':
        totp_code = request.form['totp-code']
        totp_seed = get_totp_seed(session['username'])
        totp_validate = pyotp.totp.TOTP(totp_seed)
        if totp_code != totp_validate.now():
            flash("TOTP code was invalid")
            return redirect(url_for('login_page'))
        session['authenticated'] = True
        return redirect(url_for('characters'))
    return render_template("verify-totp.html")

@app.route("/create-account", methods=['GET', 'POST'])
def create_account():
    """
    Adds an entry to the user table 
    """
    if request.method == 'POST':
        submitted_password = hash_password(request.form['password'])
        user_created = create_user(request.form['username'], submitted_password)
        if user_created:
            return redirect(url_for('login'))
        error = "Username unavailable or some other error occured"
        return render_template('create-account.html', error=error)
    authenticated = user_authenticated()
    if authenticated:
        return redirect(url_for('characters'))
    return render_template('create-account.html')

@app.route("/account")
def account_page():
    """
    Page containing buttons to either delete account or change password
    """
    if not user_authenticated():
        return redirect(url_for('login'))
    return render_template('account.html')

# @app.route("/account/delete-account")
# def delete_account():
#     """
#     Hit with DELETE request to delete account.
#     Require user to be authenticated for account to be deleted
#     """
#     return

@app.route("/account/change-password", methods=['GET', 'POST'])
def change_password():
    """
    Contains form to change password
    """
    if not user_authenticated():
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Put form data into variables
        username = session['username']
        old_password = request.form['old-password']
        new_password = request.form['new-password']
        confirm_new_password = request.form['confirm-new-password']

        # Get what the correct password should be
        hashed_password = get_password_hash(username)

        # Check if form data meets criteria
        if not correct_password(hashed_password, old_password):
            error = "Old password wrong"
            return render_template('change-password.html', error=error)
        elif old_password == new_password:
            error = "New password cannot be your old password"
            return render_template('change-password.html', error=error)
        elif new_password != confirm_new_password:
            error = "New passwords don't match"
            return render_template('change-password.html', error=error)

        # Actually update the password
        else:
            new_password_hash = hash_password(new_password)
            password_changed = change_password_hash(username, new_password_hash)
            if password_changed:
                return redirect(url_for('account_page'))
            error = "Something went wrong changing your password"
            return render_template('change-password.html', error=error)
    return render_template('change-password.html')

@app.route("/account/totp", methods=['GET', 'POST'])
def totp_page():
    """
    Lets user set up totp so they can reset their password
    """
    # No need to set up TOTP if it's already set up
    if totp_enabled(session['username']):
        flash('Your account already has totp enabled')
        return redirect(url_for('account_page'))

    # Generate new TOTP URL
    if 'totpseed' not in session:
        session['totpseed'] = pyotp.random_base32()
    totp_url = pyotp.totp.TOTP(session['totpseed']).provisioning_uri(name=session['username'], issuer_name='D&D Character Guide')

    # Validate that the TOTP code is correct
    if request.method == 'POST':
        totp_code = request.form['totp-code']
        totp_seed = session['totpseed']
        totp_validate = pyotp.totp.TOTP(totp_seed)
        if totp_code != totp_validate.now():
            error="Entered code was wrong"
            return render_template('setup-totp.html', totp_url=totp_url, error=error)
        add_totp(session['username'], session['totpseed'])
        session.pop('totpseed', None)
        flash("TOTP was successfully added")
        return redirect(url_for('account_page'))
    return render_template('setup-totp.html', totp_url=totp_url)

# @app.route("/party")
# def party_page():
#     """
#     Page containing buttons to join a party or create a party
#     """
#     return

# @app.route("/party/create")
# def create_party():
#     """
#     Page containing form to create party
#     """
#     return

# @app.route("/party/join")
# def join_party():
#     """
#     Page containing available parties to join
#     """
#     return

@app.route("/characters")
def characters():
    """
    Page containing characters in a grid
    Shows the following for each character
        - name
        - race
        - class
        - background
    Also contains buttons to view/edit/delete each character
    """
    return "You are currently authenticated"

# @app.route("/characters/show/<int:character_id>")
# def get_character_details():
#     """
#     Page to show details for a particular character
#     """
#     return

# @app.route("/characters/create")
# def create_character():
#     """
#     Page to create a new character
#     """
#     return

# @app.route("/characters/edit/<int:character_id>")
# def edit_character_details():
#     """
#     Page to edit details for a particular character
#     """
#     return

# @app.route("/characters/delete/<int:character_id>")
# def delete_character():
#     """
#     Hit with a DELETE request to delete a character
#     """
#     return


if __name__ == "__main__":
    app.run(port=8080, debug=True) # TODO: Students PLEASE remove debug=True when put in production
