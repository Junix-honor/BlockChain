import decimal
import time

from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask.json import jsonify
from flask_login import login_required, current_user

from . import exchange
from .. import db, avatars
from ..models import User, Account, CommonExchangeRecord

from ..common_deal.Bitcoin import create_deal


@exchange.before_request
@login_required
def before_request():
    if not current_user.is_certificated:
        flash('访问交易平台，请先完成实名认证！', 'info')
        return redirect(url_for('user.index'))


@exchange.route('/', methods=['GET'])
@login_required
def index():
    accounts = current_user.accounts.order_by(Account.timestamp.desc()).all()
    # common_exchange_records = CommonExchangeRecord.query.filter_by()
    common_exchange_records = []
    for account in accounts:
        common_exchange_records += account.common_exchange_records.all()
    print(common_exchange_records)
    print(accounts)
    return render_template('exchange.html', accounts=accounts, common_exchange_records=common_exchange_records)


@exchange.route('/common', methods=['POST'])
@login_required
def common():
    personal_account = current_user.accounts.filter_by(id=int(request.form.get('personal_account'))).first()
    # time.sleep(5)
    # create_deal(address_vps_one, address_vps_two, pw1, number, RPC_server):
    info = create_deal(personal_account.account_hash,
                       request.form.get("exchange_account"),
                       personal_account.chain_password,
                       decimal.Decimal(request.form.get("money")),
                       personal_account.chain_address)
    print(info)
    record = CommonExchangeRecord(exchange_account_hash=request.form.get("exchange_account"),
                                  exchange_money=float(request.form.get("money")),
                                  account=personal_account)
    db.session.add(record)
    db.session.commit()
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
