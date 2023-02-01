import json
from flask import url_for, current_app
from flask_login import current_user
from tests import conftest

from myflaskblog import create_app


def test_config():
    assert not create_app().testing
    assert create_app().testing


# def test_hello(client):
#     response = client.get('/home')
#     assert response.data == b'Write a ner post'

# def test_login(client):
#     with client.application.app_context():
#         client.application.config['SERVER_NAME'] = 'localhost'
#         client.application.config['PREFERRED_URL_SCHEME'] = 'http'
#         response = client.get(url_for('users.login'))
#         assert response.status_code == 200
# Test that the login page loads successfully

# # Test that a user can log in
# user = User(username='testuser', email='test@example.com')
# user.set_password('testpassword')
# with current_app.app_context():
#     db.session.add(user)
#     db.session.commit()
# response = client.post(url_for('users.login'), data={
#     'email': 'test@example.com',
#     'password': 'testpassword',
#     'remember_me': 'y'
# })
# assert current_user.username == 'testuser'

# # Test that a user cannot log in with an incorrect password
# response = client.post(url_for('users.login'), data={
#     'email': 'test@example.com',
#     'password': 'wrongpassword',
#     'remember_me': 'y'
# })
# assert response.status_code == 302
# assert 'Wrong email or password' in response.get_data(as_text=True)

# # Test that a user can't access the login page if already logged in
# response = client.get(url_for('users.login'))
# assert response.status_code == 302
# assert response.location == url_for('main.home', _external=True)


# def test_register(client):
#     # # Test that the registration page loads successfully
#     response = client.get(url_for('users.register'))
#     assert response.status_code == 200

# # Test that a user can register
# response = client.post(url_for('users.register'), data={
#     'username': 'testuser',
#     'email': 'test@example.com',
#     'password': 'testpassword',
#     'password2': 'testpassword'
# })
# assert response.status_code == 302
# assert response.location == url_for('users.login', _external=True)
# assert 'Welcome on board testuser' in response.get_data(as_text=True)
# with current_app.app_context():
#     user = User.query.filter_by(username='testuser').first()
#     assert user.email == 'test@example.com'
#     assert user.check_password('testpassword')

# # Test that a user can't register with a taken username
# response = client.post(url_for('users.register'), data={
#     'username': 'testuser',
#     'email': 'test2@example.com',
#     'password': 'testpassword',
#     'password2': 'testpassword'
# })
# assert response.status_code == 200
# assert 'Username already exists' in response.get_data(as_text=True)
