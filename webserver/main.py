"""
This runs the flask webserver that users will interact with

Returns:
    None?
"""
import os
import time
import json
import pyotp
from flask import Flask, session, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_qrcode import QRcode
from flask_bootstrap import Bootstrap
from dbutilities import is_user, get_password_hash, change_password_hash, create_user, delete_user, totp_enabled, add_totp, get_totp_seed, get_table_contents, add_character, add_saving_throw, add_skill, get_parties, add_party, update_user_party_id, get_user_party_id
from serverutilities import hash_password, correct_password, user_authenticated, calculate_modifier
from dotenv import load_dotenv

#used for loading json
SCRIPT_PATH = __file__

# Load environment variables from .env file to get secret
load_dotenv()

# Initialize the flask app
app = Flask(__name__)
app.secret_key = os.getenv("secret")
QRcode(app)
Bootstrap(app)

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
        return redirect(url_for('characters'))
    if request.method == 'POST':
        totp_code = request.form['totp-code']
        totp_seed = get_totp_seed(session['username'])
        totp_validate = pyotp.totp.TOTP(totp_seed)
        if totp_code != totp_validate.now():
            flash("TOTP code was invalid")
            return redirect(url_for('login'))
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

@app.route("/reset-password", methods=['GET', 'POST'])
def reset_password():
    """
    Reset user password with TOTP code
    """
    if request.method == 'POST':
        return render_template('reset-password.html')
        username = request.form['username']
        totp_code = request.form['totp-code']
        # TODO: verify the totp code
        # TODO: encrypt the new password
        # TODO: update the password for the user
    return render_template('reset-password.html')

@app.route("/account")
def account_page():
    """
    Page containing buttons to either delete account or change password
    """
    if not user_authenticated():
        return redirect(url_for('login'))
    return render_template('account.html')

@app.route("/account/delete-account", methods=['GET','POST'])
def delete_account():
    """
    Hit with DELETE request to delete account.
    Require user to be authenticated for account to be deleted
    """
    if not user_authenticated():
        return redirect(url_for('login'))
    if request.method == 'POST':
        confirmation = request.form.get('confirmation')
        if confirmation == 'yes':
            delete_user(session['username'])
            session.pop('username', None)
            session['authenticated'] = False
            flash('Account deleted')
            return redirect(url_for('index'))
        return redirect(url_for('account_page'))
    return render_template('delete-account.html')

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

@app.route("/party", methods=['GET'])
def party_page():
    """
    Page containing buttons to join a party or create a party
    """
    if not user_authenticated():
        return redirect(url_for('login'))
    user = session['username']
    partyID = get_user_party_id(user)
    party_list = get_parties()
    return render_template('party.html', party_list=party_list, partyID=partyID)

@app.route("/party/create", methods=['GET', 'POST'])
def create_party():
    """
    Page containing form to create party
    """
    if not user_authenticated():
        return redirect(url_for('login'))
    if request.method == 'POST':
        party_name = request.form['name']
        add_party(party_name)
        return redirect(url_for('join_party'))
   
    return render_template('create-party.html')

@app.route("/party/join", methods=['GET', 'POST'])
def join_party():
    """
    Page containing available parties to join
    """
    if not user_authenticated():
        return redirect(url_for('login'))
    if request.method =='POST':
        party_id = request.form['party']
        update_user_party_id(party_id, session['username'])
        return redirect(url_for('party_page'))

    party_list = get_parties()
    return render_template('join-party.html', party_list=party_list)

@app.route("/characters")
def characters():
    """
    Page containing characters in a grid
    Shows the following for each character
        - name
        - race
        - class
        - background
        - view button (approx. href /characters/show/{{ character_id }})
        - edit button (approx. href /characters/edit/{{ character_id }})
        - delete button (approx. href /characters/delete/{{ character_id }})
    """
    return "You are currently authenticated"

# @app.route("/characters/show/<int:character_id>")
# def get_character_details():
#     """
#     Page to show details for a particular character
#     """
#     return

@app.route("/characters/create", methods=['GET', 'POST'])
def create_character():
    """
    Page to create a new character
    """
    if not user_authenticated():
        return redirect(url_for('login'))

    # Get path to JSON
    data_path = os.path.dirname(os.path.dirname(SCRIPT_PATH))
    data_path = os.path.join(data_path, 'data', 'skills-and-saving-throws.json')

    # Load Skills and saving throws from JSON
    with open(data_path, encoding="utf-8") as file:
        loaded_json = json.load(file)
    abilities = loaded_json['Saving throws']
    skills = loaded_json['Skills']
    saving_throws = loaded_json['Saving throws']

    if request.method == 'POST':
        # Gather data needed to create character
        character_name = request.form['name']
        character_race = request.form['race']
        character_class = request.form['class']
        character_background = request.form['background']
        character_proficiency_bonus = int(request.form['proficiency-bonus'])
        ability_scores = []
        for ability in abilities:
            ability_scores.append(request.form[ability])
        character_id = add_character(character_name, character_race, character_class, character_background, ability_scores, character_proficiency_bonus, session['username'])

        for throw in saving_throws:
            # Determine if proficiency
            proficiency_key = f"{throw}-proficiency"
            proficiency = request.form.get(proficiency_key) == 'true'
            ability_score = int(request.form[throw])
            if proficiency:
                modifier = calculate_modifier(ability_score) + character_proficiency_bonus
            modifier = calculate_modifier(ability_score)
            add_saving_throw(character_id, throw, modifier, proficiency)

        for skill, ability_score in skills.items():
            # Determine if proficiency
            proficiency_key = f"{skill}-proficiency"
            proficiency = request.form.get(proficiency_key) == 'true'
            ability_score = int(request.form[ability_score])
            if proficiency:
                modifier = calculate_modifier(ability_score) + character_proficiency_bonus
            modifier = calculate_modifier(ability_score)
            add_skill(character_id, skill, modifier, proficiency)
        return redirect(url_for('characters'))
    races = get_table_contents('Race')
    classes = get_table_contents('Class')
    backgrounds = get_table_contents('Background')
    return render_template('create-character.html', races=races, classes=classes, backgrounds=backgrounds, saving_throws=saving_throws, skills=skills)

# @app.route("/characters/edit/<int:character_id>")
# def edit_character_details(character_id):
#     """
#     Page to edit details for a particular character
#     """
#     return

# @app.route("/characters/delete/<int:character_id>")
# def delete_character(character_id):
#     """
#     Make sure to confirm deletion, like account deletion page
#     """
#     return


if __name__ == "__main__":
    app.run(port=8080, debug=True) # TODO: Students PLEASE remove debug=True when put in production
