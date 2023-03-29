#Posts
import os
import secrets
from flask import Blueprint
from flask import render_template, url_for, redirect, flash
from myflaskblog import app, db, bcrypt
from myflaskblog.forms import RegistrationForm, LoginForm, UpdateUserForm
from myflaskblog.forms import NewPostForm
from myflaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

posts = Blueprint('posts', __name__)



@app.route("/new_post", methods=['POST', 'GET'])
@login_required
def new_post():
    # Crea un'istanza della classe "NewPostForm" definita nella sezione "forms" del codice
    form = NewPostForm()

    # Se il form viene sottomesso e passa la validazione
    if form.validate_on_submit():
        # Prende il titolo e il contenuto del post dal form
        post_title = form.post_title.data
        post_content = form.post_content.data

        # Crea un'istanza della classe "Post" definita nel database, passando il titolo, il contenuto e l'autore del post corrente
        post = Post(title=post_title,
                    post_content=post_content,
                    author=current_user)

        # Aggiunge l'istanza alla sessione del database e la commita
        db.session.add(post)
        db.session.commit()

        # Crea un messaggio flash di successo
        flash(
            f"Your post has been publiched", category="success")

        # Reindirizza l'utente alla home page dopo aver pubblicato il post
        return redirect(url_for('home'))

    # Se il form non è stato sottomesso o non ha passato la validazione, mostra la pagina "new_post" con il form per creare un nuovo post
    return render_template("new_post.html", title="New Post", form=form)


@app.route("/posts/<int:user_id>")
def posts(user_id):
    # recupera tutti i post dal database
    posts = Post.query.filter_by(user_id=user_id)

    # restituisce la pagina home.html passando come argomenti il titolo della pagina e tutti i post
    return render_template("home.html", title="Home Page", posts=posts)
