from flask import Blueprint, request, render_template
from myflaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1)
    posts = Post.query.paginate(page=page, per_page=25)
    return render_template("home.html", title="Home Page", posts=posts.items)


@main.route("/about")
def about():
    return render_template("about.html", title="About Page")
