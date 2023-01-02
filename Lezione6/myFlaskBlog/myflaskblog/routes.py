# Preparazione Lezione 5
from flask import render_template, url_for, redirect, flash
from myflaskblog import app, db, bcrypt
from myflaskblog.forms import RegistrationForm, LoginForm
from myflaskblog.models import User
from flask_login import login_user, logout_user, current_user, login_required


# from wtforms import


posts = [
    {"author": "Pico de Paperis",
     "title": "Thi is a Blog",
     "content": "This is a post by PdP. Se il post e' lunghissimo non cambia niente ?",
     "date_posted": "16-11-2022 15:48"
     },
    {"author": "Paolino Paperino",
     "title": "Qua Qua Qua",
     "content": "Paperino ha scritto in italiano",
     "date_posted": "15-11-2022 20:48"
     }
]


@app.route("/")
@app.route("/home")
def home():
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


@app.route("/new_post")
@login_required
def new_post():
    flash(f'Write a new post {current_user.username}')
    return render_template("new_post.html", title="New Post")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'Logged Out', category='info')
    return redirect('/home')
