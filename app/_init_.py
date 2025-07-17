from flask import Flask
from .models import db
from .routes import url_routes


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)
    app.register_blueprint(shortener_bp)

    with app.app_context():
        db.create_all()
    
    return app
