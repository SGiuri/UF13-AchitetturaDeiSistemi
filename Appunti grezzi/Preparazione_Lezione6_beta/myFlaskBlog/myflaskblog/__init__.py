import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import jwcrypto.jwk as jwk

# from wtforms import

app = Flask(__name__)
app.config['SECRET_KEY'] = '35f76991980ac9d1ec403f4391108054ae9ce824'
# Occhio al triplo slash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

key = jwk.JWK.generate(kty='RSA', size=2048)
app.config['JWK_KEY'] = key

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_FLASK_BLOG')
app.config['MAIL_PASSWORD'] = os.environ.get('PWD_FLASK_BLOG')
app.config['MAIL_DEFAULT_SENDER'] = 'donotreply@demo.com'

mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Pleasi Login to continue'
login_manager.login_message_category = 'danger'


# Le routes le importo dopo aver creato la app per evitare un errore di importazione circolare
from myflaskblog import routes


# Creiamo le tabelle
with app.app_context():
    db.create_all()
