# Preparazione Lezione

import os
import secrets
from flask import render_template, url_for, redirect, flash
from myflaskblog import app, db, bcrypt
from myflaskblog.forms import RegistrationForm, LoginForm, UpdateUserForm
from myflaskblog.forms import NewPostForm
from myflaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

# from wtforms import


# posts = [
#     {"author": "Pico de Paperis",
#      "title": "Thi is a Blog",
#      "content": "This is a post by PdP. Se il post e' lunghissimo non cambia niente ?",
#      "date_posted": "16-11-2022 15:48"
#      },
#     {"author": "Paolino Paperino",
#      "title": "Qua Qua Qua",
#      "content": "Paperino ha scritto in italiano",
#      "date_posted": "15-11-2022 20:48"
#      }
# ]


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()

    return render_template("home.html", title="Home Page", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About Page")


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        candidate = form.password.data
        if user and bcrypt.check_password_hash(user.password, candidate):
            login_user(user, remember=form.remember_me.data)
            flash('Welcome', category='success')
            return redirect('home')

        else:
            flash('Wrong emil or password', category='danger')
            return redirect('login')
    else:
        return render_template("login.html", title="Login Page", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        password = form.password.data
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=form.username.data,
                    password=pw_hash,
                    email=form.email.data)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        flash(
            f"Your account has been created {form.username.data}", category="success")
        return redirect('/login')

    return render_template("register.html", title="Register Page", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'Logged Out', category='info')
    return redirect('/home')


@app.route("/user_account")
@login_required
def user_account():
    image_file = url_for(
        'static', filename=f"images/{current_user.image_file}")

    return render_template("user_account.html", title=f"{current_user.username} page",
                           image_file=image_file)


@app.route("/user_account/edit", methods=['POST', 'GET'])
@login_required
def edit_user_account():
    image_file = url_for(
        'static', filename=f"images/{current_user.image_file}")

    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.image_file.data:
            new_file_name = save_image_file(form.image_file.data)
            current_user.image_file = new_file_name

        if current_user.username != form.username.data:
            current_user.username = form.username.data

        if current_user.email != form.email.data:
            current_user.email = form.email.data

        db.session.commit()

        flash(
            f"Your account has been updated {form.username.data}", category="success")
        return redirect(url_for('user_account'))
    else:

        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("edit_user_account.html", title=f"{current_user.username} update page",
                           image_file=image_file, form=form)


def save_image_file(image_file_data):

    _, file_ext = os.path.splitext(image_file_data.filename)

    new_name = secrets.token_hex(8)
    new_file_name = new_name + file_ext
    file_path = os.path.join(os.getcwd(), "myflaskblog",
                             "static", "images", new_file_name)

    image_file_data.save(file_path)
    # todo: cancellare l'immagine vecchia (os)
    # todo: ridurre le dimensioni di quelle che sto caricande (pillo)
    return new_file_name


@app.route("/new_post", methods=['POST', 'GET'])
@login_required
def new_post():
    form = NewPostForm()

    if form.validate_on_submit():
        post_title = form.post_title.data
        post_content = form.post_content.data

        post = Post(title=post_title,
                    post_content=post_content,
                    author=current_user)

        db.session.add(post)
        db.session.commit()
        flash(
            f"Your post has been publiched", category="success")
        return redirect(url_for('home'))

    return render_template("new_post.html", title="New Post", form=form)
