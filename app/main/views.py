import os

from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user

from . import main
from .forms import *
from .. import db, avatars
from ..models import User, Account


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    accounts = current_user.accounts.order_by(Account.timestamp.desc()).all()
    common_exchange_records = []
    for account in accounts:
        common_exchange_records += account.common_exchange_records.all()
    return render_template('index.html', accounts=accounts, common_exchange_records=common_exchange_records)
