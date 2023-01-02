from flask import render_template, url_for, redirect, flash
from myflaskblog import db, app, bcrypt
from myflaskblog.forms import RegistrationForm, LoginForm
from myflaskblog.models import User

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
        if form.email.data == "simone.giuri@gmail.com" and form.password.data == "password":
            flash(f"Welcome back {form.email.data}", category="info")
            return redirect('/home')
        else:
            flash(f"Wrong email and password", category="danger")
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


@app.route("/new_post")
def new_post():
    return render_template("new_post.html", title="New Post")
