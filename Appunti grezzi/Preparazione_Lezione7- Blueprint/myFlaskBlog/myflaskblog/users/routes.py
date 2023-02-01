from flask import render_template, url_for, redirect, flash, request, Blueprint, current_app
from myflaskblog import db, bcrypt
from myflaskblog.users.forms import RegistrationForm, LoginForm, UpdateForm, PasswordRecoveryRequestForm, ResetPasswordForm
from myflaskblog.models import User
from flask_login import login_user, login_required, logout_user, current_user
from myflaskblog.users.utils import send_email, save_picture


users = Blueprint('users', __name__)


@users.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mail.home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        candidate_pwd = form.password.data
        if user and bcrypt.check_password_hash(user.password, candidate_pwd):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {user.username}', category='info')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash('Worng email or password', category='danger')
            return redirect('/login')

    else:
        return render_template("login.html", title="Login Page", form=form)


@users.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    password=hashed_pwd,
                    email=form.email.data)
        with current_app.app_context():

            db.session.add(user)
            db.session.commit()

        flash(f"Welcome on board {form.username.data}", category="success")
        return redirect('/login')

    return render_template("register.html", title="Register Page", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash('User logged out', category='info')

    return redirect('/home')


@users.route("/user_profile")
@login_required
def user_profile():
    image_file = url_for(
        'static', filename=f"profile_pic/{current_user.image_file}")

    return render_template("user_profile.html",
                           title=f"{current_user.username} page",
                           image_file=image_file)


@users.route("/user_profile/update", methods=['POST', 'GET'])
@login_required
def edit_user_profile():

    form = UpdateForm()
    image_file = url_for(
        'static', filename=f"profile_pic/{current_user.image_file}")
    if (current_user.username != form.username.data) or (
            current_user.email != form.email.data) or (
            form.image_file.data):
        if form.validate_on_submit():

            with current_app.app_context():
                if form.image_file.data:
                    new_file_name = save_picture(form.image_file.data)
                    current_user.image_file = new_file_name
                current_user.username = form.username.data
                current_user.email = form.email.data
                db.session.commit()

                flash(
                    f"Profile updated for user {current_user.username}", category="success")
            return redirect('/user_profile')
        else:
            form.username.data = current_user.username
            form.email.data = current_user.email
        return render_template("edit_user_profile.html",
                               title=f"{current_user.username} page",
                               image_file=image_file, form=form)

    return render_template("edit_user_profile.html",
                           title=f"{current_user.username} page",
                           image_file=image_file, form=form)


@users.route("/passwordrecovery", methods=['POST', 'GET'])
def passwordrecovery():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = PasswordRecoveryRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user)
            flash(f"Email sent to {user.email}", category="success")
        else:
            flash(f"Email sent to {form.email.data}", category="success")
        return redirect(url_for('main.home'))

    return render_template("passwordrecovery.html", title="Recover your Password", form=form)


# NOT WORKING
@users.route("/passwordrecovery/<token>", methods=['POST', 'GET'])
def resetpassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user_id = User.verify_reset_token(token)

    if user_id is None:
        flash('Invalid reset request', category='warning')
        return redirect(url_for('users.passwordrecovery'))

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
