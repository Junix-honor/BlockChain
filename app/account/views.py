import os

from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask.json import jsonify
from flask_login import login_required, current_user
import base64

from . import account
from .. import db, avatars
from ..models import User, Account


@account.route('/', methods=['GET'])
@login_required
def index():
    # accounts = Account.query.filter_by().order_by(Account.timestamp.desc()).all()
    accounts = current_user.accounts.order_by(Account.timestamp.desc()).all()
    print(accounts)
    return render_template('account.html', accounts=accounts)


# 添加账户
@account.route('/add', methods=['POST'])
@login_required
def add():
    account = Account(chain_address=request.form.get("chain_address"),
                      chain_password=request.form.get("chain_password"),
                      account_hash=request.form.get("account_hash"),
                      account_alias=request.form.get("account_alias"),
                      pay_password=request.form.get("pay_password"),
                      across_chain=True
                      if request.form.get("across_chain") == 'true'
                      else False,
                      user=current_user._get_current_object())
    db.session.add(account)
    db.session.commit()
    return redirect(url_for("account.index"))


# 检查address是否存在
@account.route('/validate/chain_address', methods=['POST'])
def validate_chain_address():
    # TODO: 验证地址是否存在
    return jsonify(True)


# 检查chain_address-account_hash是否已经用过
@account.route('/validate/account_hash', methods=['POST'])
def validate_account_hash():
    if Account.query.filter_by(chain_address=request.form.get('chain_address'),
                               account_hash=request.form.get('account_hash')).first():
        return jsonify(False)
    return jsonify(True)


# 检查account_alias是否已经用过
@account.route('/validate/account_alias', methods=['POST'])
def validate_account_alias():
    if Account.query.filter_by(account_alias=request.form.get('account_alias')).first():
        return jsonify(False)
    return jsonify(True)
