import os
from flask import Flask
from app.extension import db, LoginManager, bcrypt
from app.models import User, Game
from app.core.routes import core_bp
from app.users.routes import user_bp    
from app.games.routes import games_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)
    LoginManager.init_app(app)
    LoginManager.login_view = 'users.login'
    LoginManager.login_message_category = 'danger'
    LoginManager.login_message = 'Please login to access this page.'
    bcrypt.init_app(app)

    app.register_blueprint(core_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(games_bp, url_prefix='/games')

    return app