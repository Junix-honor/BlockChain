import os
from app import create_app
from app import db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

