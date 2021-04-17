from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    id_card = db.Column(db.String(18), unique=True, index=True)
    avatar = db.Column(db.Text())
    card_front = db.Column(db.Text())
    card_back = db.Column(db.Text())
    password = db.Column(db.String(128))
    pay_password = db.Column(db.String(6))
    phone = db.Column(db.String(11))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    signature = db.Column(db.Text())
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    is_certificated = db.Column(db.Integer(), default=0)
    accounts = db.relationship('Account', backref='user', lazy='dynamic')

    def verify_password(self, password):
        return self.password == password

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def certificate(self):
        self.is_certificated = 1

    def __repr__(self):
        return '<User %r>' % self.username


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chain_address = db.Column(db.String(128))
    chain_password = db.Column(db.String(128))
    account_hash = db.Column(db.String(128))
    account_alias = db.Column(db.String(128))
    pay_password = db.Column(db.String(128))
    across_chain = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
