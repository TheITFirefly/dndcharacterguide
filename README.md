# Milestone 3 setup
This readme is meant to show that all of us have proper access to the git repo for IT&C 350's project. Just add your name to the list once you've accepted the invite to be a collaborator

## Group members
- Stephen Snow
- Alex Olmsted
- Thomas Noble
- Zachary Hansen

# Developing
Jordan's template for is available at [this github repo](https://github.com/jordanbw1/itc350-template/blob/main/main.py) and may be helpful as a reference as we figure out the templating and stuff for ourselves. You may also want to look at the [flask quick start](https://flask.palletsprojects.com/en/2.3.x/quickstart). Finally it is recommended that you run `python -c 'import secrets; print(secrets.token_hex())'` for generating the secret in the .env file

## Development setup overview
1. clone the repo, preferably on your own branch
2. install mariadb
3. create a database for the project
4. create a user for said database identified by a password and grant all privileges on database.* Don't forget to flush_privileges just in case
5. Log in to the project database as the project user, source the database-setup script from the repo
6. Set up the .env
7. set up a venv with python 3.12 and install dependencies using the requirements.txt
8. Run the python script for importing races,classes, backgrounds
9. Enjoy your new flask application

# TODO

- [ ] Characters overview
- [ ] Editing individual characters
- [ ] Deleting characters
- [ ] Password resets
- [ ] Party creation
- [ ] Party joining
- [ ] Party deletion?
- [ ] Party member management? (May require database schema change to add party admin status)
- [ ] Improved setup instructions in readme (see signal list sent to Alex for a rough idea)

## Helpful resources
- [Editing/deleting characters](https://flask.palletsprojects.com/en/2.3.x/quickstart/#variable-rules)