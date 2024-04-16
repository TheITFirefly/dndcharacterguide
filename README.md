# Milestone 3 setup
This readme is meant to show that all of us have proper access to the git repo for IT&C 350's project. Just add your name to the list once you've accepted the invite to be a collaborator

## Group members
- Stephen Snow
- Alex Olmsted
- Thomas Noble
- Zachary Hansen

# Developing
You may want to look at the [flask quick start](https://flask.palletsprojects.com/en/2.3.x/quickstart) for information on flask. It's really cool, and there is a lot that can be done with flask. It is also strongly recommended that you run `python -c 'import secrets; print(secrets.token_hex())'` for generating the secret in the .env file. And finally, don't forget that main is not dev. Please set up your own branch if you want to contribute

## Development setup overview
1. clone the repo, preferably on your own branch
2. install mariadb server
3. create a database for the project
4. create a user for said database identified by a password and grant all privileges on database.* Don't forget to flush_privileges just in case
5. Log in to the project database as the project user, source the database-setup script from the repo
6. Set up the .env
7. set up a venv with python 3.12 and install dependencies using the requirements.txt. You may need to intall the python 3.12 development package to get this working
8. Run the python script for importing races, classes, and backgrounds
9. Enjoy your new flask application

# TODONE

- [X] Characters overview
- [X] Viewing individual characters
- [X] Editing individual characters
- [X] Deleting characters
- [X] Password resets
- [X] Party creation
- [X] Party joining
- [X] Improved setup instructions in readme

## Helpful resources
- [Editing/deleting characters](https://flask.palletsprojects.com/en/2.3.x/quickstart/#variable-rules)