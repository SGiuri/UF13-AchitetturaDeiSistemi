import pytest
import os
import jwcrypto.jwk as jwk

from myflaskblog import create_app, db

from flask.testing import FlaskClient

key = jwk.JWK.generate(kty='RSA', size=2048)


class Config:

    # '35f76991980ac9d1ec403f4391108054ae9ce824'
    SECRET_KEY = os.environ.get('SECRET_KEY_FLASK_BLOG')
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    JWK_KEY = key
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_FLASK_BLOG')
    MAIL_PASSWORD = os.environ.get('PWD_FLASK_BLOG')
    MAIL_DEFAULT_SENDER = 'donotreply@demo.com'


@pytest.fixture()
def app():
    app = create_app()

    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
