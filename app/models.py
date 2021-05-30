from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager
from .help import help


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(10), unique=True, index=True)
    id_card = db.Column(db.String(18), index=True)
    avatar = db.Column(db.String(64))
    # card_front = db.Column(db.Text())
    # card_back = db.Column(db.Text())
    password_hash = db.Column(db.String(128))
    pay_password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(11))
    name = db.Column(db.String(30))
    location = db.Column(db.String(64))
    signature = db.Column(db.String(100))
    about_me = db.Column(db.String(200))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    is_certificated = db.Column(db.Boolean, default=False)
    accounts = db.relationship('Account', backref='user', lazy='dynamic')
    # 密保
    # protection_question = db.Column(db.String(128))
    # protection_answer_hash = db.Column(db.String(128))

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

    # 密保哈希
    @property
    def protection_answer(self):
        raise AttributeError('protection_answer is not a readable attribute')

    @protection_answer.setter
    def protection_answer(self, answer):
        self.protection_answer_hash = generate_password_hash(answer)

    def verify_protection_answer(self, answer):
        return check_password_hash(self.protection_answer_hash, answer)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def certificate(self):
        self.is_certificated = True

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
    is_independent_password = db.Column(db.Boolean, default=False)
    pay_password_hash = db.Column(db.String(128))
    across_chain = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    common_exchange_records = db.relationship('CommonExchangeRecord', backref='account', lazy='dynamic')

    # money
    @property
    def money(self):
        return float(round(help.Query_Balance(self.chain_address, self.account_hash), 2))

    @money.setter
    def money(self, value):
        raise AttributeError('money is not a editable attribute')

    # pay_password哈希
    @property
    def pay_password(self):
        raise AttributeError('pay_password is not a readable attribute')

    @pay_password.setter
    def pay_password(self, password):
        self.pay_password_hash = generate_password_hash(password)

    def verify_pay_password(self, password):
        if self.is_independent_password:
            return check_password_hash(self.pay_password_hash, password)
        else:
            return self.user.verify_pay_password(password)


class CommonExchangeRecord(db.Model):
    __tablename__ = 'common_exchange_records'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    exchange_account_hash = db.Column(db.String(128))
    exchange_money = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class CrossExchangeRecord(db.Model):
    __tablename__ = 'cross_exchange_records'
    id = db.Column(db.Integer, primary_key=True)
    in_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    in_account = db.relationship('Account', foreign_keys=[in_account_id])
    out_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    out_account = db.relationship('Account', foreign_keys=[out_account_id])
    exchange_in_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    exchange_in_account = db.relationship('Account', foreign_keys=[exchange_in_account_id])
    exchange_out_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    exchange_out_account = db.relationship('Account', foreign_keys=[exchange_out_account_id])
    exchange_money = db.Column(db.Float)
    hash_clock = db.Column(db.String(128))
    request_contract_address = db.Column(db.String(128))
    respond_contract_address = db.Column(db.String(128))
    status = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # 判断交易是否处于否活动状态
    def active(self):
        if 0 < self.status < 4:
            return True
        else:
            return False

    # 判断交易是否结束
    def finished(self):
        if self.status == 4 or self.status < 0:
            return True
        else:
            return False

    def need_requester(self):
        if self.status == 2 or self.status == 3 or self.status == 4:
            return True
        else:
            return False

    def need_responder(self):
        if self.status == 1:
            return True
        else:
            return False

    # 判断id是否为发起方userid
    def is_request(self, userid):
        return self.out_account.user.id == userid

    # 判断id是否为发起方userid
    def is_respond(self, userid):
        return self.exchange_out_account.user.id == userid

    def set_initialized(self):
        self.status = 1

    def is_initialized(self):
        return self.status == 1

    def set_agreed(self):
        self.status = 2

    def is_agreed(self):
        return self.status == 2

    def set_encrypted(self):
        self.status = 3

    def is_encrypted(self):
        return self.status == 3

    def set_validated(self):
        self.status = 4

    def is_validated(self):
        return self.status == 4

    def is_succeeded(self):
        return self.status == 4

    def set_canceled(self):
        self.status = -self.status

    def is_canceled(self):
        return self.status < 0

    def page_status(self):
        return self.status


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
