from flask import Blueprint

cross_exchange = Blueprint('cross_exchange', __name__)

from . import views
