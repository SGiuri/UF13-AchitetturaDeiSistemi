from flask import Flask, render_template, url_for

app = Flask(__name__)

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


@app.route("/login")
def login():
    return render_template("login.html", title="Login Page")


@app.route("/register")
def register():
    return render_template("register.html", title="Register Page")


@app.route("/new_post")
def new_post():
    return render_template("new_post.html", title="New Post")
