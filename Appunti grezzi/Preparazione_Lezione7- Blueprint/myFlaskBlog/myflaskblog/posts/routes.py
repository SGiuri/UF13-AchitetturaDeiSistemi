from flask import render_template, redirect, flash, Blueprint, current_app, url_for, abort
from myflaskblog import db
from myflaskblog.posts.forms import Edit_Post_Form, New_Post_Form
from myflaskblog.models import Post, User
from flask_login import login_required, current_user


posts = Blueprint('posts', __name__)


@posts.route("/new_post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = New_Post_Form()
    if form.validate_on_submit():
        post_title = form.title.data
        post_content = form.post_content.data

        new_post = Post(title=post_title,
                        post_content=post_content, user_id=current_user.id)
        with current_app.app_context():

            db.session.add(new_post)
            db.session.commit()

        flash(f"New Message Posted!", category="success")
        return redirect('/home')

    return render_template("new_post.html", title="New Post", form=form)


@posts.route("/home/<int:post_id>")
def a_post(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template("home.html", title=f"{post.title}", posts=[post])


@posts.route("/home/<int:post_id>/edit", methods=['POST', 'GET'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = Edit_Post_Form()
    if form.validate_on_submit():
        if form.submit.data == True:
            post.title = form.title.data
            post.post_content = form.post_content.data

            db.session.commit()
            flash(f"Message Updated!", category="success")
            return redirect(url_for('posts.a_post', post_id=post_id))
        if form.delete.data == True:

            return redirect(url_for('posts.delete_confirmationa_post', post_id=post_id))

    else:
        form.title.data = post.title
        form.post_content.data = post.post_content

        return render_template("edit_post.html", title="Edit Post", form=form, post_id=post_id, rusure=False)


@posts.route("/home/<int:post_id>/confirm", methods=['POST', 'GET'])
@login_required
def delete_confirmationa_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = Edit_Post_Form()
    if form.validate_on_submit():

        if form.rusure.data == True:

            return redirect(url_for('posts.delete_post', post_id=post_id))
    else:
        form.title.data = post.title
        form.post_content.data = post.post_content

        return render_template("edit_post.html", title="Edit Post", form=form, post_id=post_id, rusure=True)


@posts.route("/home/<string:author_username>", methods=['POST', 'GET'])
def an_author_posts(author_username):
    user = User.query.filter_by(username=author_username).first()
    posts = Post.query.filter_by(user_id=user.id)
    return render_template("home.html", title=f"{author_username} post's", posts=posts)


@posts.route("/home/<int:post_id>/delete_post", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post Deleted!", category="success")
    return redirect(url_for('main.home'))
