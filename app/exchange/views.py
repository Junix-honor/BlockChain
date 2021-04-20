import os
import time

from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask.json import jsonify
from flask_login import login_required, current_user
import base64

from . import exchange
from .. import db, avatars
from ..models import User, Account

from ..common_deal.Bitcoin import create_deal


@exchange.route('/', methods=['GET'])
@login_required
def index():
    accounts = current_user.accounts.order_by(Account.timestamp.desc()).all()
    print(accounts)
    return render_template('exchange.html', accounts=accounts)


@exchange.route('/common', methods=['POST'])
@login_required
def common():
    personal_account = current_user.accounts.filter_by(id=int(request.form.get('personal_account'))).first()
    # time.sleep(5)
    create_deal(personal_account.account_hash,
                request.form.get("exchange_account"),
                personal_account.chain_password,
                request.form.get("money"),
                personal_account.chain_address)
    return jsonify({"code": 1000, "message": "交易成功"})


# # 检查exchange_account是否存在
# @exchange.route('/validate/exchange_account', methods=['POST'])
# def validate_exchange_account():
#     personal_account = current_user.accounts.filter_by(id=int(request.form.get('personal_account'))).first()
#     print(personal_account.chain_address)
#     if Account.query.filter_by(account_hash=request.form.get('exchange_account'),
#                                chain_address=personal_account.chain_address).first():
#         return jsonify(True)
#     else:
#         return jsonify(False)


# 检查exchange_account是否是当前用户
@exchange.route('/validate/same_user_account', methods=['POST'])
def validate_same_user_account():
    personal_account = current_user.accounts.filter_by(id=int(request.form.get('personal_account'))).first()
    print(personal_account.chain_address)
    if current_user.accounts.filter_by(account_hash=request.form.get('exchange_account'),
                                       chain_address=personal_account.chain_address).first():
        return jsonify(False)
    else:
        return jsonify(True)


@exchange.route('/validate/validate_password', methods=['POST'])
def validate_password():
    personal_account = current_user.accounts.filter_by(id=int(request.form.get('personal_account'))).first()
    print(personal_account.chain_address)
    if personal_account.verify_pay_password(request.form.get('password')):
        return jsonify(True)
    else:
        return jsonify(False)
