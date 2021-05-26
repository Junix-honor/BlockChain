import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_AVATARS_DEST = os.path.join(basedir, 'app\\static\\images\\avatar')
    UPLOADED_CARDS_DEST = os.path.join(basedir, 'app\\static\\images\\card')
    UPLOADED_AVATARS_ALLOW = ['png', 'jpg', 'gif']
    UPLOADED_CARDS_ALLOW = ['png', 'jpg', 'gif']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                           'mysql+pymysql://%s:%s@127.0.0.1:3306/%s' % ('root', '', 'blockchain')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    #                           'mysql://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                           'mysql+pymysql://%s:%s@127.0.0.1:3306/%s' % ('root', '', 'blockchain')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
