from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads
from flask_login import LoginManager
from config import config
from .filters import ID, STATUS

id_code = ID()
exchange_status = STATUS()
bootstrap = Bootstrap()
db = SQLAlchemy()
avatars = UploadSet('AVATARS')
cards = UploadSet('CARDS')
moment = Moment()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    id_code.init_app(app)
    exchange_status.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    configure_uploads(app, [avatars, cards])

    # db.drop_all()
    # db.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .exchange import exchange as exchange_blueprint
    app.register_blueprint(exchange_blueprint, url_prefix='/common_exchange')

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    from .cross_exchange import cross_exchange as cross_exchange_blueprint
    app.register_blueprint(cross_exchange_blueprint, url_prefix='/cross_exchange')

    return app
