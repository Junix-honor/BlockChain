import os

from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask.json import jsonify
from flask_login import login_required, current_user

from . import user
from .. import db, avatars
from ..models import User, Account


@user.route('/', methods=['GET'])
@login_required
def index():
    return render_template('user.html')


# 修改头像
@user.route('/avatar', methods=['POST'])
def avatar():
    if current_user.avatar:
        os.remove(avatars.path(current_user.avatar))
    if 'avatar' not in request.files:
        flash('图片上传错误', 'error')
        return redirect(url_for('user.index'))
    filename = current_user.username + request.files['avatar'].filename[-4:]
    avatars.save(request.files['avatar'], name=filename)
    current_user.avatar = filename
    db.session.add(current_user._get_current_object())
    db.session.commit()
    return redirect(url_for('user.index'))


# 修改信息
@user.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == 'GET':
        return jsonify({"code": 1000,
                        "username": current_user.username,
                        "location": current_user.location,
                        "signature": current_user.signature,
                        "about_me": current_user.about_me
                        })
    else:
        current_user.username = request.form.get("username")
        current_user.signature = request.form.get("signature")
        current_user.location = request.form.get("location")
        current_user.about_me = request.form.get("about_me")
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('个人信息更新成功', 'success')
        return redirect(url_for('user.index'))


# 修改密码
@user.route('/password', methods=['POST'])
def password_change():
    current_user.password = request.form.get("password")
    db.session.add(current_user._get_current_object())
    db.session.commit()
    flash('密码修改成功', 'success')
    return redirect(url_for('user.index'))


# 实名认证
@user.route('/certification', methods=['POST'])
def certification():
    current_user.name = request.form.get("name")
    current_user.id_card = request.form.get("id_card")
    current_user.phone = request.form.get("phone")
    current_user.pay_password = request.form.get("pay_password")
    current_user.certificate()
    db.session.add(current_user._get_current_object())
    db.session.commit()
    flash('实名验证成功', 'success')
    return redirect(url_for('user.index'))


# 实名认证
@user.route('/certification_edit', methods=['POST'])
def certification_edit():
    current_user.name = request.form.get("edit_name")
    current_user.id_card = request.form.get("edit_id_card")
    current_user.phone = request.form.get("edit_phone")
    db.session.add(current_user._get_current_object())
    db.session.commit()
    flash('实名验证修改成功', 'success')
    return redirect(url_for('user.index'))


# 修改支付密码
@user.route('/pay_password', methods=['POST'])
def pay_password_change():
    current_user.pay_password = request.form.get("edit_pay_password")
    db.session.add(current_user._get_current_object())
    db.session.commit()
    flash('支付密码修改成功', 'success')
    return redirect(url_for('user.index'))


# 检查密码是否正确
@user.route('/validate/password', methods=['POST'])
def validate_password():
    if current_user.verify_password(password=request.form.get("old_password")):
        return jsonify(True)
    else:
        return jsonify(False)


# 检查支付密码是否正确
@user.route('/validate/pay_password', methods=['POST'])
def validate_pay_password():
    if current_user.verify_pay_password(password=request.form.get("old_pay_password")):
        return jsonify(True)
    else:
        return jsonify(False)


# 检查用户名是否存在
@user.route('/validate/username', methods=['POST'])
def validate_username():
    account = User.query.filter_by(username=request.form.get('username')).first()
    if account and account.id != current_user.id:
        return jsonify(False)
    return jsonify(True)
