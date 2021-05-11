import os

from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user

from . import main
from .. import db, avatars
from ..models import User, Account, CommonExchangeRecord, CrossExchangeRecord


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    accounts = current_user.accounts.order_by(Account.timestamp.desc()).all()
    common_exchange_records = db.session.query(CommonExchangeRecord). \
        join(Account, Account.id == CommonExchangeRecord.account_id). \
        filter(Account.user_id == current_user.id). \
        order_by(CommonExchangeRecord.timestamp.desc()).all()
    send = db.session.query(CrossExchangeRecord). \
        join(Account, Account.id == CrossExchangeRecord.in_account_id). \
        join(User, User.id == Account.user_id). \
        filter(Account.user_id == current_user.id). \
        order_by(CrossExchangeRecord.timestamp.desc()).all()
    receive = db.session.query(CrossExchangeRecord). \
        join(Account, Account.id == CrossExchangeRecord.exchange_in_account_id). \
        join(User, User.id == Account.user_id). \
        filter(Account.user_id == current_user.id). \
        order_by(CrossExchangeRecord.timestamp.desc()).all()
    cross_exchange_records = receive + send
    # wallet_num
    wallet_num = current_user.accounts.count()
    # exchange_num
    exchange_num = len(common_exchange_records) + len(cross_exchange_records)
    # total_in
    total_in = 0
    for record in receive:
        if record.is_succeeded():
            total_in += record.exchange_money
    # total_out
    total_out = 0
    for record in common_exchange_records:
        if record.is_succeeded():
            total_out += record.exchange_money
    for record in send:
        if record.is_succeeded():
            total_in += record.exchange_money
    return render_template('index.html', accounts=accounts, common_exchange_records=common_exchange_records,
                           cross_exchange_records=cross_exchange_records, wallet_num=wallet_num,
                           exchange_num=exchange_num, total_in=total_in, total_out=total_out)
