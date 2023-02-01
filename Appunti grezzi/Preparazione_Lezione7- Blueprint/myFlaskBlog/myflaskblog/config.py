import os
import jwcrypto.jwk as jwk

key = jwk.JWK.generate(kty='RSA', size=2048)

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY_FLASK_BLOG')# '35f76991980ac9d1ec403f4391108054ae9ce824'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_FLASK_BLOG') # 'sqlite:///mydb.db'
    JWK_KEY = key
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_FLASK_BLOG')
    MAIL_PASSWORD = os.environ.get('PWD_FLASK_BLOG')
    MAIL_DEFAULT_SENDER = 'donotreply@demo.com'