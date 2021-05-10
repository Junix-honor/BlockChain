import time

from flask import render_template, redirect, url_for, flash, request
from flask.json import jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import aliased

from . import cross_exchange
from .. import db
from ..models import Account, CrossExchangeRecord, User
from .pyte import callsh
from urllib.parse import urlparse
from .callfx import *


@cross_exchange.before_request
@login_required
def before_request():
    if not current_user.is_certificated:
        flash('访问交易平台，请先完成实名认证！', 'info')
        return redirect(url_for('user.index'))


@cross_exchange.route('/', methods=['GET'])
@login_required
def index():
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
    print(send)
    print(receive)
    exchanges = receive + send
    return render_template('cross_exchange.html', exchanges=exchanges)


@cross_exchange.route('/process', methods=['GET', 'POST'])
@login_required
def process():
    accounts = current_user.accounts.order_by(Account.timestamp.desc()).all()
    if 'id' in request.args:
        record = CrossExchangeRecord.query.filter_by(id=request.args['id']).first()
        return render_template('cross_process.html', accounts=accounts, record=record)
    return render_template('cross_process.html', accounts=accounts, record=None)


@cross_exchange.route('/account', methods=['POST'])
@login_required
def account_info():
    account = current_user.accounts.filter_by(id=int(request.form.get('id'))).first()
    return jsonify({"code": 1000, "chain_address": account.chain_address, "account_hash": account.account_hash,
                    "money": account.money})


@cross_exchange.route('/initiate', methods=['GET', 'POST'])
@login_required
def initiate():
    out_account = current_user.accounts.filter_by(id=int(request.form.get('out_account'))).first()
    in_account = current_user.accounts.filter_by(id=int(request.form.get('in_account'))).first()
    # 寻找匹配的账户  exchange_in_account exchange_out_account
    account1 = aliased(Account)
    account2 = aliased(Account)
    res = db.session.query(account1.id, account2.id, account1.money, account2.money). \
        join(account2, account1.user_id == account2.user_id). \
        filter(account1.user_id != current_user.id). \
        filter(account1.across_chain == 1). \
        filter(account2.across_chain == 1). \
        filter(account1.chain_address == in_account.chain_address). \
        filter(account2.chain_address == out_account.chain_address). \
        order_by(account1.money.desc()).first()
    print(res)
    if res is None:
        return jsonify({"code": 5000, "message": "交易匹配失败"})
    else:
        record = CrossExchangeRecord(in_account=in_account, out_account=out_account,
                                     exchange_in_account_id=res[1],
                                     exchange_out_account_id=res[0],
                                     exchange_money=float(request.form.get("money")))
        record.set_initialized()
        db.session.add(record)
        db.session.commit()
        # return redirect(url_for('cross_exchange.process', id=record.id))
        return jsonify({"code": 1000, "message": "交易发起成功", "id": record.id})


@cross_exchange.route('/agree', methods=['POST'])
@login_required
def agree():
    # print(request.form.get('id'))
    record = CrossExchangeRecord.query.filter_by(id=int(request.form.get('id'))).first()
    # 发起账户部署
    _url = urlparse(record.out_account.chain_address)
    print(record.out_account.account_hash, record.exchange_in_account.account_hash,
          float(record.exchange_money), _url.hostname, _url.port)
    request_contract_address = callsh(record.out_account.account_hash, record.exchange_in_account.account_hash,
                                      float(record.exchange_money), _url.hostname, _url.port)
    record.request_contract_address = request_contract_address
    # 匹配账户部署
    _url = urlparse(record.exchange_out_account.chain_address)
    print(record.exchange_out_account.account_hash, record.in_account.account_hash,
          float(record.exchange_money), _url.hostname, _url.port)
    respond_contract_address = callsh(record.exchange_out_account.account_hash, record.in_account.account_hash,
                                      float(record.exchange_money), _url.hostname, _url.port)
    record.respond_contract_address = respond_contract_address
    record.set_agreed()
    db.session.add(record)
    db.session.commit()
    return jsonify({"code": 1000, "message": "交易部署成功"})


@cross_exchange.route('/encrypt', methods=['POST'])
@login_required
def encrypt():
    record = CrossExchangeRecord.query.filter_by(id=int(request.form.get('record_id_encrypt'))).first()
    print(record)
    print(request.form.get('private_key'))
    # TODO：设置HASH锁
    # request  contract
    _url = urlparse(record.out_account.chain_address)
    calladdlock(record.out_account.account_hash, request.form.get('private_key'),
                record.out_account.chain_password,
                _url.hostname, _url.port, record.request_contract_address)
    # respond contract
    _url = urlparse(record.exchange_out_account.chain_address)
    calladdlock(record.exchange_out_account.account_hash, request.form.get('private_key'),
                record.exchange_out_account.chain_password,
                _url.hostname, _url.port, record.respond_contract_address)
    record.hash_clock = request.form.get('private_key')
    print("encrypt sucess")
    record.set_encrypted()
    db.session.add(record)
    db.session.commit()
    return jsonify({"code": 1000, "message": "交易加密成功"})


@cross_exchange.route('/validate', methods=['GET', 'POST'])
@login_required
def validate():
    record = CrossExchangeRecord.query.filter_by(id=int(request.form.get('record_id_validate'))).first()
    record.set_validated()
    # TODO：交易验证
    # request  contract
    _url = urlparse(record.in_account.chain_address)
    print("step1")
    print(record.in_account.account_hash, request.form.get('validate_private_key'),
          record.in_account.chain_password,
          _url.hostname, _url.port, record.respond_contract_address)
    callunlock(record.in_account.account_hash, request.form.get('validate_private_key'),
               record.in_account.chain_password,
               _url.hostname, _url.port, record.respond_contract_address)
    # respond contract
    _url = urlparse(record.exchange_in_account.chain_address)
    print("step2")
    print(record.exchange_in_account.account_hash, request.form.get('validate_private_key'),
          record.exchange_in_account.chain_password,
          _url.hostname, _url.port, record.request_contract_address)
    callunlock(record.exchange_in_account.account_hash, request.form.get('validate_private_key'),
               record.exchange_in_account.chain_password,
               _url.hostname, _url.port, record.request_contract_address)
    db.session.add(record)
    db.session.commit()
    return jsonify({"code": 1000, "message": "交易验证成功"})


@cross_exchange.route('/cancel', methods=['POST'])
@login_required
def cancel():
    print(request.form.get('id'))
    record = CrossExchangeRecord.query.filter_by(id=int(request.form.get('id'))).first()
    record.set_canceled()
    db.session.add(record)
    db.session.commit()
    return jsonify({"code": 1000, "message": "交易取消成功"})


# @exchange.route('/common', methods=['POST'])
# @login_required
# def common():
#     personal_account = current_user.accounts.filter_by(id=int(request.form.get('personal_account'))).first()
#     time.sleep(5)
#     # create_deal(address_vps_one, address_vps_two, pw1, number, RPC_server):
#     info = create_deal(personal_account.account_hash,
#                        request.form.get("exchange_account"),
#                        personal_account.chain_password,
#                        decimal.Decimal(request.form.get("money")),
#                        personal_account.chain_address)
#     print(info)
#     record = CommonExchangeRecord(exchange_account_hash=request.form.get("exchange_account"),
#                                   exchange_money=request.form.get("money"),
#                                   account=personal_account)
#     db.session.add(record)
#     db.session.commit()
#     return jsonify({"code": 1000, "message": "交易成功"})
#
#
# @exchange.route('/cross', methods=['POST', 'GET'])
# @login_required
# def cross():
#     return render_template('cross_process.html')


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


# # 检查exchange_account是否是当前用户
# @exchange.route('/validate/same_user_account', methods=['POST'])
# def validate_same_user_account():
#     personal_account = current_user.accounts.filter_by(id=int(request.form.get('personal_account'))).first()
#     print(personal_account.chain_address)
#     if current_user.accounts.filter_by(account_hash=request.form.get('exchange_account'),
#                                        chain_address=personal_account.chain_address).first():
#         return jsonify(False)
#     else:
#         return jsonify(True)
#
#

# 检查交易密码是否正确
@cross_exchange.route('/validate/validate_password', methods=['POST'])
def validate_password():
    account = current_user.accounts.filter_by(id=int(request.form.get('account'))).first()
    if account.verify_pay_password(request.form.get('password')):
        return jsonify(True)
    else:
        return jsonify(False)


# 检查交易金额是否超过帐号余额
@cross_exchange.route('/validate/money', methods=['POST'])
def validate_money():
    account = current_user.accounts.filter_by(id=int(request.form.get('id'))).first()
    if float(request.form.get('money')) > account.money:
        return jsonify(False)
    else:
        return jsonify(True)


# 检查转出账户和转入账户是否在同一个链上
@cross_exchange.route('/validate/same_blockchain', methods=['POST'])
def validate_same_blockchain():
    out_account = current_user.accounts.filter_by(id=int(request.form.get('out_account'))).first()
    in_account = current_user.accounts.filter_by(id=int(request.form.get('in_account'))).first()
    if out_account.chain_address == in_account.chain_address:
        return jsonify(False)
    else:
        return jsonify(True)
