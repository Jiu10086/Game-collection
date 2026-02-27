import os
from flask import Flask
from pokemon.extension import db, LoginManager, bcrypt
from pokemon.models import User, Type, Pokemon
from pokemon.core.routes import core_bp
from pokemon.users.routes import user_bp    
from pokemon.pokemon.routes import pokemon_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)
    LoginManager.init_app(app)
    LoginManager.login_view = 'users.login'
    LoginManager.login_message_category = 'danger'
    LoginManager.login_message = 'Bro try na type routes'
    bcrypt.init_app(app)

    app.register_blueprint(core_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(pokemon_bp, url_prefix='/pokemon')

    return app