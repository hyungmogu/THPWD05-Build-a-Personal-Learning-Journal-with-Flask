from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


class JournalEntryForm(Form):
    title = StringField(
        'Title',
        [
            DataRequired()
        ]
    )
    date = DateField(
        'Date'
    )
    time_spent = IntegerField(
        'Time Spent',
        [
            NumberRange(min=0)
        ]
    )
    learned = TextAreaField(
        'What I Learend'
    )
    resources = TextAreaField(
        'Resources To Remember'
    )