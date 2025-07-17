import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/url_shortener'
SQLALCHEMY_TRACK_MODIFICATIONS = False
