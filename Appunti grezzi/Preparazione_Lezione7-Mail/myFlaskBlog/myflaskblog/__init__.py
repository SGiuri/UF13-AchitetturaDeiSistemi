from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '35f76991980ac9d1ec403f4391108054ae9ce824'
# Occhio al triplo slash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from myflaskblog import routes

# Creiamo le tabelle
with app.app_context():
    db.create_all()
