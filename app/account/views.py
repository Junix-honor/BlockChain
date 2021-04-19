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


# 编辑账户
@account.route('/edit', methods=['POST', 'GET'])
@login_required
def edit():
    if request.method == 'GET':
        account = current_user.accounts.filter_by(id=int(request.args.get("edit_id"))).first()
        if account:
            return jsonify({"code": 1000,
                            "chain_address": account.chain_address,
                            "chain_password": account.chain_password,
                            "account_hash": account.account_hash,
                            "account_alias": account.account_alias,
                            "pay_password": account.pay_password,
                            "across_chain": account.across_chain
                            })
        else:
            return jsonify({"code": 5000})
    else:
        account = current_user.accounts.filter_by(id=int(request.form.get("account_id"))).first()
        print(account)
        print(request.form.get("account_id"))
        account.chain_address = request.form.get("edit_chain_address")
        account.chain_password = request.form.get("edit_chain_password")
        account.account_hash = request.form.get("edit_account_hash")
        account.account_alias = request.form.get("edit_account_alias")
        account.pay_password = request.form.get("edit_pay_password")
        account.across_chain = True if request.form.get("edit_across_chain") == 'true' else False
        db.session.add(account)
        db.session.commit()
        return redirect(url_for("account.index"))


# 删除账户
@account.route('/delete', methods=['POST'])
@login_required
def delete():
    # print(request.form.get("delete_id"))
    current_user.accounts.filter_by(id=request.form.get("delete_id")).delete()
    db.session.commit()
    return jsonify({"code": 1000, "message": "删除成功！"})


# 检查address是否存在
@account.route('/validate/chain_address', methods=['POST'])
def validate_chain_address():
    # TODO: 验证地址是否存在
    return jsonify(True)


# 检查chain_address-account_hash是否已经用过
@account.route('/validate/account_hash', methods=['POST'])
def validate_account_hash():
    account_id = int(request.form.get('account_id'))
    account = Account.query.filter_by(chain_address=request.form.get('chain_address'),
                                      account_hash=request.form.get('account_hash')).first()
    if account:
        if account_id and account.id == account_id:
            return jsonify(True)
        else:
            return jsonify(False)
    return jsonify(True)


# 检查account_alias是否已经用过
@account.route('/validate/account_alias', methods=['POST'])
def validate_account_alias():
    account_id = int(request.form.get('account_id'))
    account = Account.query.filter_by(account_alias=request.form.get('account_alias')).first()
    if account:
        if account_id and account.id == account_id:
            return jsonify(True)
        else:
            return jsonify(False)
    return jsonify(True)
