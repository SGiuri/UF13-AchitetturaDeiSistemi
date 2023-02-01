import os
import secrets
from flask import render_template, url_for, redirect, flash, request
from myflaskblog import db, app, bcrypt, login_manager, mail
from myflaskblog.forms import RegistrationForm, LoginForm, UpdateForm, New_Post_Form, PasswordRecoveryRequestForm, ResetPasswordForm
from myflaskblog.models import User, Post
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1)
    posts = Post.query.paginate(page=page, per_page=5)
    return render_template("home.html", title="Home Page", posts=posts.items)


@app.route("/about")
def about():
    return render_template("about.html", title="About Page")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        candidate_pwd = form.password.data
        if user and bcrypt.check_password_hash(user.password, candidate_pwd):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {user.username}', category='info')
            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash('Worng email or password', category='danger')
            return redirect('/login')

    else:
        return render_template("login.html", title="Login Page", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    password=hashed_pwd,
                    email=form.email.data)
        with app.app_context():

            db.session.add(user)
            db.session.commit()

        flash(f"Welcome on board {form.username.data}", category="success")
        return redirect('/login')

    return render_template("register.html", title="Register Page", form=form)


@app.route("/new_post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = New_Post_Form()
    if form.validate_on_submit():
        post_title = form.title.data
        post_content = form.post_content.data

        new_post = Post(title=post_title,
                        post_content=post_content, user_id=current_user.id)
        with app.app_context():

            db.session.add(new_post)
            db.session.commit()

        flash(f"New Message Posted!", category="success")
        return redirect('/home')

    return render_template("new_post.html", title="New Post", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('User logged out', category='info')

    return redirect('/home')


@app.route("/user_profile")
@login_required
def user_profile():
    update = False
    image_file = url_for(
        'static', filename=f"profile_pic/{current_user.image_file}")

    return render_template("user_profile.html",
                           title=f"{current_user.username} page",
                           image_file=image_file, update=update)


def save_picture(form_file_data):
    new_file_name = secrets.token_hex(6)
    _, file_ext = os.path.splitext(form_file_data.filename)
    file_name = new_file_name + file_ext
    file_path = os.path.join(app.root_path, 'static/profile_pic', file_name)

    form_file_data.save(file_path)
    return file_name


@app.route("/user_profile/update", methods=['POST', 'GET'])
@login_required
def user_profile_update():
    update = True
    form = UpdateForm()
    image_file = url_for(
        'static', filename=f"profile_pic/{current_user.image_file}")
    if (current_user.username != form.username.data) or (
            current_user.email != form.email.data) or (
            form.image_file.data):
        if form.validate_on_submit():

            with app.app_context():
                if form.image_file.data:
                    new_file_name = save_picture(form.image_file.data)
                    current_user.image_file = new_file_name
                current_user.username = form.username.data
                current_user.email = form.email.data
                db.session.commit()

                flash(
                    f"Profile updated for user {current_user.username}", category="success")
            return redirect('/user_profile')

    return render_template("user_profile.html",
                           title=f"{current_user.username} page",
                           image_file=image_file, update=update, form=form)


@app.route("/passwordrecovery", methods=['POST', 'GET'])
def passwordrecovery():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = PasswordRecoveryRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user)
            flash(f"Email sent to {user.email}", category="success")
        else:
            flash(f"Email sent to {form.email.data}", category="success")
        return redirect(url_for('home'))

    return render_template("passwordrecovery.html", title="Recover your Password", form=form)


# WORKING
# @app.route("/passwordrecovery/<token>", methods=['POST', 'GET'])
# def resetpassword(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     user_from_token = User.verify_reset_token(token)

#     if user_from_token is None:
#         flash('Invalid reset request', category='warning')
#         return redirect(url_for('passwordrecovery'))

#     form = ResetPasswordForm()

#     if form.validate_on_submit():
#         login_user(user_from_token)
#         hashed_pwd = bcrypt.generate_password_hash(
#             form.password.data).decode('utf-8')
#         with app.app_context():
#             current_user.password = hashed_pwd
#             db.session.commit()
#             logout_user()
#             flash(
#                 f"Password reset completed for {user_from_token.username}", category="success")

#         return redirect('/login')

#     return render_template("resetpassword.html", title="Reset your password", form=form)


# NOT WORKING
@app.route("/passwordrecovery/<token>", methods=['POST', 'GET'])
def resetpassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user_id = User.verify_reset_token(token)

    if user_id is None:
        flash('Invalid reset request', category='warning')
        return redirect(url_for('passwordrecovery'))

    user = User.query.filter_by(id=user_id).first()

    form = ResetPasswordForm()

    if form.validate_on_submit():

        hashed_pwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # with app.app_context():
        user.password = hashed_pwd

        db.session.commit()

        flash(
            f"Password reset completed for {user.username}", category="success")

        return redirect('/login')

    return render_template("resetpassword.html", title="Reset your password", form=form)


def send_email(user):
    token = user.generate_reset_token(90)

    msg = Message("Password Reset",
                  recipients=[user.email])
    msg.body = f'''
        To reset your password click in the link:
        {url_for('resetpassword', token=token, _external=True)}

        If you didin't request a pasword reset, simply ignore this message.
    '''
    print(msg.body)  # for debugging printing message in console instead of sending the email

    # mail.send(msg)

# @login_manager.unauthorized_handler
# def unauthorized_handler():

#     flash('Please login to acces this page', category='danger')
#     return redirect(url_for('login'))
