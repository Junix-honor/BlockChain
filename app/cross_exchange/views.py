import time

from flask import render_template, redirect, url_for, flash, request
from flask.json import jsonify
from flask_login import login_required, current_user

from . import cross_exchange
from .. import db
from ..models import Account, CrossExchangeRecord


@cross_exchange.before_request
@login_required
def before_request():
    if not current_user.is_certificated:
        flash('访问交易平台，请先完成实名认证！', 'info')
        return redirect(url_for('user.index'))


@cross_exchange.route('/', methods=['GET'])
@login_required
def index():
    send = []
    receive = []
    for account in current_user.accounts:
        send += CrossExchangeRecord.query.filter_by(in_account=account).order_by(
            CrossExchangeRecord.timestamp.desc()).all()
        receive += CrossExchangeRecord.query.filter_by(exchange_in_account=account).order_by(
            CrossExchangeRecord.timestamp.desc()).all()
    active_exchanges = receive + send
    return render_template('cross_exchange.html', active_exchanges=active_exchanges)


@cross_exchange.route('/process', methods=['GET', 'POST'])
@login_required
def process():
    accounts = current_user.accounts.order_by(Account.timestamp.desc()).all()
    if 'id' in request.args:
        record = CrossExchangeRecord.query.filter_by(id=request.args['id']).first()
        return render_template('cross_process.html', accounts=accounts, record=record)
    return render_template('cross_process.html', accounts=accounts, record=None)


@cross_exchange.route('/request/step1', methods=['GET', 'POST'])
@login_required
def request_step1():
    out_account = current_user.accounts.filter_by(id=int(request.form.get('out_account'))).first()
    in_account = current_user.accounts.filter_by(id=int(request.form.get('in_account'))).first()
    # TODO:寻找匹配的账户  exchange_in_account exchange_out_account
    time.sleep(10)
    record = CrossExchangeRecord(in_account=in_account, out_account=out_account,
                                 exchange_in_account=None,
                                 exchange_out_account=None,
                                 exchange_money=float(request.form.get("money")))
    record.set_request_step1()
    db.session.add(record)
    db.session.commit()
    # return redirect(url_for('cross_exchange.process', id=record.id))
    return jsonify({"code": 1000, "message": "交易发起成功", "id": record.id})


@cross_exchange.route('/respond/step1', methods=['GET', 'POST'])
@login_required
def respond_step1():
    record = CrossExchangeRecord.query.filter_by(id=int(request.form.get('id'))).first()
    record.set_respond_step1()
    db.session.add(record)
    db.session.commit()
    return jsonify({"code": 1000, "message": "交易同意成功"})


@cross_exchange.route('/request/step2', methods=['GET', 'POST'])
@login_required
def request_step2():
    record = CrossExchangeRecord.query.filter_by(id=int(request.form.get('record_id_private_key'))).first()
    record.private_key = request.form.get('private_key')
    record.set_request_step2()
    # TODO: 检查并部署合约到链2
    record.set_respond_step2()
    db.session.add(record)
    db.session.commit()
    return redirect(url_for('cross_exchange.process', id=record.id))


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
@cross_exchange.route('/validate/validate_password', methods=['POST'])
def validate_password():
    out_account = current_user.accounts.filter_by(id=int(request.form.get('out_account'))).first()
    if out_account.verify_pay_password(request.form.get('password')):
        return jsonify(True)
    else:
        return jsonify(False)
