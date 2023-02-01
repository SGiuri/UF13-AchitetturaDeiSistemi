import os
import secrets

from flask import url_for, current_app
from myflaskblog import mail
from flask_mail import Message


def save_picture(form_file_data):
    new_file_name = secrets.token_hex(6)
    _, file_ext = os.path.splitext(form_file_data.filename)
    file_name = new_file_name + file_ext
    file_path = os.path.join(current_app.root_path,
                             'static/profile_pic', file_name)

    form_file_data.save(file_path)
    return file_name


def send_email(user):
    token = user.generate_reset_token(90)

    msg = Message("Password Reset",
                  recipients=[user.email])
    msg.body = f'''
        To reset your password click in the link:
        {url_for('users.resetpassword', token=token, _external=True)}

        If you didin't request a pasword reset, simply ignore this message.
    '''
    print(msg.body)  # for debugging printing message in console instead of sending the email
    mail.send(msg)
