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
# [x] Contains a Peewee model class for adding and editing journal entries
# 3. Listing Page
# [] List page shows journal entries where each entry displays with their respective title and date/time created
# 4. Detail Page
# [x] Detail page shows:
#     1. Title
#     2. Date
#     3. Time Spent
#     4. What You Learned
#     5. Resources to Remember
# 5. Add/Edit Page
# [x] Add/Edit page enables the user to post new entries or edit existing entries with all of the following fields:
#     1. Title
#     2. Date
#     3. Time Spent
#     4. What You Learned
#     5. Resources to Remember
# 6. Delete Entry
# [] Ability to delete an entry
# 7. Styling
# [x] Each section of the journal entry uses the correct CSS from the supplied file: Entry itself, Title, Date, Time Spent, What You Learned, Resources to Remember
# 8. Routing
# [x] All routes are mapped correctly and use correct HTTP methods:
#     1. / and /entries
#     2. /entries/new
#     3. /entries/{id}
#     4. /entries/{id}/edit
#     5. /entries/{id}/delete
# 9. Python Coding Style
# [] The code is clean, readable, and well organized. It complies with most common PEP 8 standards of style.

from flask import (
    Flask, render_template,
    flash, redirect, url_for, g, request, abort)

import forms
import models

DEBUG = True
HOST = "0.0.0.0"
PORT = 8000

app = Flask(__name__)
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = True

app.secret_key = 'Hello world. This part can be any random but very secret string'


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('index.html', entries=entries)


@app.route('/entries')
def entries():
    return redirect(url_for('index'))


@app.route('/entries/<int:entry_id>')
def entry_detail(entry_id):
    entry = None

    # Fetch entry by id
    try:
        entry = models.Entries.select().where(
            models.Entries.id == int(entry_id)
        ).get()
    except models.DoesNotExist:
        abort(404)

    return render_template('detail.html', entry=entry)


@app.route('/entries/new', methods=('GET', 'POST'))
def create_entry():
    form = forms.JournalEntryForm()

    if form.validate_on_submit():

        entry_id = models.Entries.create_entry(
            title=form.title.data.strip(),
            date=form.date.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data.strip(),
            resources=form.resources.data.strip(),
        )

        return redirect(url_for('entry_detail', entry_id=entry_id))

    return render_template('new.html', form=form)


@app.route('/entries/<int:entry_id>/edit', methods=('GET', 'POST'))
def edit_entry(entry_id):
    entry = None

    form = forms.JournalEntryForm()

    try:
        entry = models.Entries.select().where(
            models.Entries.id == int(entry_id)
        ).get()
    except models.DoesNotExist:
        abort(404)

    # Fetch entry by id
    if request.method == 'GET':
        form.title.data = entry.title
        form.date.data = entry.date
        form.time_spent.data = entry.time_spent
        form.learned.data = entry.learned
        form.resources.data = entry.resources

    else:
        # If information is valid, then update data
        if form.validate_on_submit():
            entry.title = form.title.data.strip()
            entry.date = form.date.data
            entry.time_spent = form.time_spent.data
            entry.learned = form.learned.data.strip()
            entry.resources = form.resources.data.strip()
            entry.save()

            flash("Update is successful")

            # if update is successful, return to detail page
            return redirect(url_for('entry_detail', entry_id=entry_id))

    return render_template('edit.html', form=form, entry_id=entry_id)


@app.route('/entries/<int:entry_id>/delete')
def delete_entry(entry_id):
    # Fetch entry by id
    try:
        entry = models.Entries.get(models.Entries.id == int(entry_id))
        entry.delete()
        flash("Entry has been deleted successfully")
    except models.DoesNotExist:
        # if entry is none, then flash a message
        flash("Entry doesn't exist")

    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)