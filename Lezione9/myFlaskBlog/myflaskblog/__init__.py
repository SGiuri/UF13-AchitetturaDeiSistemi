from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from myflaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Occhio al triplo slash

def create_app(config_object = Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.__init__(app)
    bcrypt.__init__(app)
    login_manager.__init__(app)


    from myflaskblog.users.routes import users
    from myflaskblog.posts.routes import posts
    from myflaskblog.main.routes import main    

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app