from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

import datetime

DATABASE = SqliteDatabase('sample.db')


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)
    name = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("User Already Exists")


class Entries(Model):
    user = ForeignKeyField(User, related_name="author")
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = CharField(max_length=10)
    learned = TextField()
    resources = TextField()
    shell = CharField(max_length=100)
    extras = TextField()

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entries], safe=True)
    DATABASE.close()