from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
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
    password_hash = db.Column(db.String(128))
    pay_password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(11))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    signature = db.Column(db.Text())
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    is_certificated = db.Column(db.Integer(), default=0)
    accounts = db.relationship('Account', backref='user', lazy='dynamic')

    # password哈希
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # pay_password哈希
    @property
    def pay_password(self):
        raise AttributeError('pay_password is not a readable attribute')

    @pay_password.setter
    def pay_password(self, password):
        self.pay_password_hash = generate_password_hash(password)

    def verify_pay_password(self, password):
        return check_password_hash(self.pay_password_hash, password)

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
    pay_password_hash = db.Column(db.String(128))
    across_chain = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    money = db.Column(db.Float)
    common_exchange_records = db.relationship('CommonExchangeRecord', backref='account', lazy='dynamic')

    # pay_password哈希
    @property
    def pay_password(self):
        raise AttributeError('pay_password is not a readable attribute')

    @pay_password.setter
    def pay_password(self, password):
        self.pay_password_hash = generate_password_hash(password)

    def verify_pay_password(self, password):
        if self.is_independent_pay_password():
            return check_password_hash(self.pay_password_hash, password)
        else:
            return self.user.verify_pay_password(password)

    def is_independent_pay_password(self):
        return True if self.pay_password_hash else False


class CommonExchangeRecord(db.Model):
    __tablename__ = 'common_exchange_records'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    exchange_account_hash = db.Column(db.String(128))
    exchange_money = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
