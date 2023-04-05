
from flask import render_template

from flask import Blueprint
from myflaskblog.users.forms import LoginForm
from myflaskblog.posts.forms import NewPostForm
from myflaskblog.users.forms import RegistrationForm
from myflaskblog.users.forms import UpdateUserForm
from myflaskblog.models import Post


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    # recupera tutti i post dal database
    all_posts = Post.query.all()

    # restituisce la pagina home.html passando come argomenti il titolo della pagina e tutti i post
    return render_template("home.html", title="Home Page", posts=all_posts)


@main.route("/about")
def about():
    # restituisce la pagina about.html passando come argomento il titolo della pagina
    return render_template("about.html", title="About Page")

