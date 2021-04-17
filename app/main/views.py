import os

from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user
import base64

from . import main
from .forms import *
from .. import db, avatars
from ..models import User, Account


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    edit = EditProfileForm()
    password = EditPasswordForm()
    certification = CertificationForm()
    if edit.submit1.data and edit.validate_on_submit():
        if edit.avatar.data:
            if current_user.avatar:
                os.remove(avatars.path(current_user.avatar))
            filename = current_user.username + edit.avatar.data.filename[-4:]
            avatars.save(edit.avatar.data, name=filename)
            current_user.avatar = filename
        current_user.signature = edit.signature.data
        current_user.location = edit.location.data
        current_user.about_me = edit.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.user'))
    if password.submit2.data and password.validate_on_submit():
        current_user.password = password.password.data
        print(password.password.data)
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('main.user'))
    if certification.submit3.data and certification.validate_on_submit():
        current_user.name = certification.name.data
        current_user.id_card = certification.id.data
        current_user.phone = certification.phone.data
        current_user.certificate()
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('提交成功.', 'success')
        return redirect(url_for('main.user'))
    edit.signature.data = current_user.signature
    edit.location.data = current_user.location
    edit.about_me.data = current_user.about_me
    return render_template('user.html', edit=edit, password=password, certification=certification)
