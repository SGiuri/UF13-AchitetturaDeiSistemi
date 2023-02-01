from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from myflaskblog.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


login_manager.login_view = 'users.login'
login_manager.login_message = 'Please Login to continue'
login_manager.login_message_category = 'danger'


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    mail.__init__(app)
    db.__init__(app)
    bcrypt.__init__(app)
    login_manager.__init__(app)

    from myflaskblog.users.routes import users
    from myflaskblog.posts.routes import posts
    from myflaskblog.main.routes import main
    from myflaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
    # # Creiamo le tabelle
    # with app.app_context():
    #     db.create_all()
