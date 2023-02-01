# Lezione 5
from datetime import datetime, timedelta
import python_jwt as jwt
from flask import current_app
from myflaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(30), nullable=False,
                           default="default_img.jpg")
    posts = db.relationship('Post', backref="author", lazy=True)

    def generate_reset_token(self, expire_sec=1800):
        payload = {'user_id': self.id}
        return jwt.generate_jwt(payload, current_app.config['JWK_KEY'], 'PS256', timedelta(seconds=expire_sec))

    @staticmethod
    def verify_reset_token(jwk_token):
        try:
            _, claims = jwt.verify_jwt(
                jwk_token, current_app.config['JWK_KEY'], ['PS256'])
            print(claims)
            user_id = claims['user_id']
        except:
            return None
        return user_id

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    post_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.date_posted}', '{self.user_id}')"
