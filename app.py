# REQUIREMENTS
# ============
#
# 1. Dependency File
# [x] Included a requirements/dependencies file
#       - FLASK
#       - Peewee
#           - pip install peewee
#       - Flask-Login
#           - pip install flask-login
#       - Flask-bcrypt
#           - pip install flask-bcrypt
#       - Flask-wtf
#           - pip install Flask-WTF
#     NOTE: This will be either a requirements.txt file or a Pipfile
# 2. Peewee Model Classes
# [] Contains a Peewee model class for adding and editing journal entries
# 3. Listing Page
# [] List page shows journal entries where each entry displays with their respective title and date/time created
# 4. Detail Page
# [] Detail page shows:
#     1. Title
#     2. Date
#     3. Time Spent
#     4. What You Learned
#     5. Resources to Remember
# 5. Add/Edit Page
# [] Add/Edit page enables the user to post new entries or edit existing entries with all of the following fields:
#     1. Title
#     2. Date
#     3. Time Spent
#     4. What You Learned
#     5. Resources to Remember
# 6. Delete Entry
# [] Ability to delete an entry
# 7. Styling
# [] Each section of the journal entry uses the correct CSS from the supplied file: Entry itself, Title, Date, Time Spent, What You Learned, Resources to Remember
# 8. Routing
# [] All routes are mapped correctly and use correct HTTP methods:
#     1. / and /entries
#     2. /entries/new
#     3. /entries/{id}
#     4. /entries/{id}/edit
#     5. /entries/{id}/delete
# 9. Python Coding Style
# [] The code is clean, readable, and well organized. It complies with most common PEP 8 standards of style.

from flask import (
    Flask, g, abort, render_template,
    flash, redirect, url_for, request)
from flask_bcrypt import check_password_hash
from flask_login import (
    LoginManager, login_user, current_user,
    login_required, logout_user)

import forms
import models

DEBUG = True
HOST = "0.0.0.0"
PORT = 8000

app = Flask(__name__)
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = True

app.secret_key = 'Hello world. This part can be any random but very secret string'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)