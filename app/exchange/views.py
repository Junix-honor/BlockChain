import decimal

from flask import render_template, redirect, url_for, flash, request
from flask.json import jsonify
from flask_login import login_required, current_user

from . import exchange
from .. import db
from ..models import Account, CommonExchangeRecord, User

from .deal import create_deal
from ..help import help


@exchange.before_request
@login_required
def before_request():
    if not current_user.is_certificated:
        flash('访问交易平台，请先完成实名认证！', 'info')
        return redirect(url_for('user.index'))


@exchange.route('/', methods=['GET'])
@login_required
def index():
    common_exchange_records = db.session.query(CommonExchangeRecord). \
        join(Account, Account.id == CommonExchangeRecord.account_id). \
        filter(Account.user_id == current_user.id). \
        order_by(CommonExchangeRecord.timestamp.desc()).all()
    accounts = current_user.accounts.order_by(Account.timestamp.desc()).all()
    return render_template('exchange.html', accounts=accounts, common_exchange_records=common_exchange_records)


@exchange.route('/common', methods=['POST'])
@login_required
def common():
    personal_account = current_user.accounts.filter_by(id=int(request.form.get('personal_account'))).first()
    # time.sleep(5)
    # 地址错误返回-2，交易错误返回-1，正常退出返回0
    # create_deal(address_vps_one, address_vps_two, pw1, number, RPC_server):
    info = create_deal(personal_account.account_hash,
                       request.form.get("exchange_account"),
                       personal_account.chain_password,
                       decimal.Decimal(request.form.get("money")),
                       personal_account.chain_address)
    if info == -3:
        return jsonify({"code": 5000, "message": "余额不足"})
    elif info == -2:
        return jsonify({"code": 5000, "message": "地址错误"})
    elif info == -1:
        return jsonify({"code": 5000, "message": "交易错误"})
    else:
        record = CommonExchangeRecord(exchange_account_hash=request.form.get("exchange_account"),
                                      exchange_money=float(request.form.get("money")),
                                      account=personal_account)
        db.session.add(record)
        db.session.commit()
        return jsonify({"code": 1000, "message": "交易成功"})


@exchange.route('/account', methods=['POST'])
@login_required
def account_info():
    account = current_user.accounts.filter_by(id=int(request.form.get('id'))).first()
    return jsonify({"code": 1000, "chain_address": account.chain_address, "account_hash": account.account_hash,
                    "money": account.money})


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

# 检查交易金额是否超过帐号余额
@exchange.route('/validate/money', methods=['POST'])
def validate_money():
    account = current_user.accounts.filter_by(id=int(request.form.get('id'))).first()
    if float(request.form.get('money')) > account.money:
        return jsonify(False)
    else:
        return jsonify(True)


# 检查exchange_account是否是当前用户
@exchange.route('/validate/same_user_account', methods=['POST'])
def validate_same_user_account():
    personal_account = current_user.accounts.filter_by(id=int(request.form.get('personal_account'))).first()
    # print(personal_account.chain_address)
    if current_user.accounts.filter_by(account_hash=request.form.get('exchange_account'),
                                       chain_address=personal_account.chain_address).first():
        return jsonify(False)
    else:
        return jsonify(True)


@exchange.route('/validate/validate_password', methods=['POST'])
def validate_password():
    personal_account = current_user.accounts.filter_by(id=int(request.form.get('personal_account'))).first()
    # print(personal_account.chain_address)
    if personal_account.verify_pay_password(request.form.get('password')):
        return jsonify(True)
    else:
        return jsonify(False)
