# Lezione 4 Finita


from datetime import datetime
from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

# from wtforms import

app = Flask(__name__)
app.config['SECRET_KEY'] = '35f76991980ac9d1ec403f4391108054ae9ce824'
# Occhio al triplo slash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(30), nullable=False,
                           default="default_img.jpg")
    posts = db.relationship('Post', backref="author", lazy=True)

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


# Creiamo le tabelle
with app.app_context():
    db.create_all()


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
        with app.app_context():
            user = User(username=form.username.data,
                        password=form.password.data,
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()

        flash(f"Welcome on board {form.username.data}", category="success")
        return redirect('/login')

    return render_template("register.html", title="Register Page", form=form)


@app.route("/new_post")
def new_post():
    return render_template("new_post.html", title="New Post")


if __name__ == '__main__':
    app.run(debug=True)
