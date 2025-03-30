from django.contrib.sessions.backends import db


class User:
    def save (self):
        db.session.add (self)
        db.session.commit()
    def __init__(self, username: str):
        self.username = username
