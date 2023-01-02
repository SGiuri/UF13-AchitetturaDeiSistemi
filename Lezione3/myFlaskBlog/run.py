# Lezione 3

from flask import Flask, render_template, url_for, redirect

from forms import RegistrationForm, LoginForm

# from wtforms import

app = Flask(__name__)
app.config['SECRET_KEY'] = '35f76991980ac9d1ec403f4391108054ae9ce824'

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
        print('You Are Logged In')
        return redirect('/home')

    else:
        return render_template("login.html", title="Login Page", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        print('Registered')
        return redirect('/login')

    return render_template("register.html", title="Register Page", form=form)


@app.route("/new_post")
def new_post():
    return render_template("new_post.html", title="New Post")


if __name__ == '__main__':
    app.run(debug=True)
