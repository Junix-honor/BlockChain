from flask import render_template, redirect, request, url_for, flash
from flask.json import jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user is not None and user.verify_password(password=request.form.get("password")):
            print(request.form.get("remember_me"))
            login_user(user, request.form.get("remember_me"))
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('用户名或密码错误', 'error')
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(email=request.form.get("email"),
                    username=request.form.get("username"),
                    password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html')


# 检查username是否已经用过
@auth.route('/validate/username', methods=['POST'])
def validate_username():
    if User.query.filter_by(username=request.form.get('username')).first():
        return jsonify(False)
    return jsonify(True)


# 检查email是否已经注册
@auth.route('/validate/email', methods=['POST'])
def validate_email():
    if User.query.filter_by(email=request.form.get('email')).first():
        return jsonify(False)
    return jsonify(True)
