import os

from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask.json import jsonify
from flask_login import login_required, current_user
import base64

from . import account
from .. import db, avatars
from ..models import User, Account
from ..help import help


@account.before_request
@login_required
def before_request():
    if not current_user.is_certificated:
        flash('访问个人帐号，请先完成实名认证！', 'info')
        return redirect(url_for('user.index'))


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
                      is_independent_password=True
                      if request.form.get("independent_password") == 'true'
                      else False,
                      user=current_user._get_current_object(),
                      money=help.Query_Balance(request.form.get("chain_address"), request.form.get("account_hash")))
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
        account.across_chain = True if request.form.get("edit_across_chain") == 'true' else False
        db.session.add(account)
        db.session.commit()
        return redirect(url_for("account.index"))


# 修改密码
@account.route('/password', methods=['POST'])
@login_required
def password():
    account = current_user.accounts.filter_by(id=int(request.form.get("password_account_id"))).first()
    account.is_independent_password = True if request.form.get("edit_independent_password") == 'true' else False
    account.pay_password = request.form.get("edit_password")
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


# 检查密码是否正确
@account.route('/validate/password', methods=['POST'])
def validate_password():
    print(request.form.get('password_account_id'))
    print(request.form.get('old_password'))
    account = Account.query.filter_by(id=int(request.form.get('password_account_id'))).first()
    if account and account.verify_pay_password(password=request.form.get('old_password')):
        return jsonify(True)
    else:
        return jsonify(False)


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
