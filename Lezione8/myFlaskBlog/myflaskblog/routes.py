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
    # recupera tutti i post dal database
    posts = Post.query.all()

    # restituisce la pagina home.html passando come argomenti il titolo della pagina e tutti i post
    return render_template("home.html", title="Home Page", posts=posts)


@app.route("/about")
def about():
    # restituisce la pagina about.html passando come argomento il titolo della pagina
    return render_template("about.html", title="About Page")


@app.route("/login", methods=['POST', 'GET'])
def login():
    # crea un oggetto LoginForm()
    form = LoginForm()

    if form.validate_on_submit():
        # cerca l'utente nel database usando l'email inserita nel form
        user = User.query.filter_by(email=form.email.data).first()
        candidate = form.password.data
        # controlla che l'utente esista e che la password inserita sia corretta
        if user and bcrypt.check_password_hash(user.password, candidate):
            # se la password è corretta, effettua il login e reindirizza alla pagina home
            login_user(user, remember=form.remember_me.data)
            flash('Welcome', category='success')
            return redirect('home')
        else:
            # altrimenti mostra un messaggio di errore e reindirizza alla pagina di login
            flash('Wrong email or password', category='danger')
            return redirect('login')
    else:
        # restituisce la pagina di login passando il titolo della pagina e il form per effettuare il login
        return render_template("login.html", title="Login Page", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    # crea un oggetto RegistrationForm()
    form = RegistrationForm()

    if form.validate_on_submit():
        # crea un hash della password inserita e salva l'utente nel database
        password = form.password.data
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=form.username.data,
                    password=pw_hash,
                    email=form.email.data)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        # mostra un messaggio di successo e reindirizza alla pagina di login
        flash(
            f"Your account has been created {form.username.data}", category="success")
        return redirect('/login')

    # restituisce la pagina di registrazione passando il titolo della pagina e il form
    # per registrarsi
    return render_template("register.html", title="Register Page", form=form)


@app.route("/logout")
@login_required
def logout():
    # effettua il logout e mostra un messaggio di info
    logout_user()
    flash(f'Logged Out', category='info')
    return redirect('/home')


@app.route("/user_account")
@login_required
def user_account():
    # crea l'url per l'immagine del profilo dell'utente
    image_file = url_for(
        'static', filename=f"images/{current_user.image_file}")

    # restituisce la pagina user_account.html passando il titolo della pagina, l'url dell'immagine
    # del profilo dell'utente
    return render_template("user_account.html", title=f"{current_user.username} page",
                           image_file=image_file)

@app.route("/user_account/edit", methods=['POST', 'GET'])
@login_required
def edit_user_account():
    # Percorso del file immagine dell'utente
    image_file = url_for('static', filename=f"images/{current_user.image_file}")

    # Creazione del form per l'aggiornamento dei dati dell'utente
    form = UpdateUserForm()

    if form.validate_on_submit():
        # Aggiornamento del file immagine dell'utente se presente
        if form.image_file.data:
            new_file_name = save_image_file(form.image_file.data)
            current_user.image_file = new_file_name

        # Aggiornamento del nome utente se diverso dal precedente
        if current_user.username != form.username.data:
            current_user.username = form.username.data

        # Aggiornamento dell'email utente se diversa da quella precedente
        if current_user.email != form.email.data:
            current_user.email = form.email.data

        # Salvataggio dei dati aggiornati nel database
        db.session.commit()

        # Messaggio di conferma per l'utente
        flash(f"I tuoi dati sono stati aggiornati {form.username.data}", category="success")
        return redirect(url_for('user_account'))
    else:
        # Se il form non è stato validato, riempire i campi del form con i dati dell'utente
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Mostra la pagina di modifica dati utente
    return render_template("edit_user_account.html", title=f"{current_user.username} - Pagina di aggiornamento dati",
                           image_file=image_file, form=form)


def save_image_file(image_file_data):
    # Estrae l'estensione del file immagine
    _, file_ext = os.path.splitext(image_file_data.filename)

    # Crea un nuovo nome univoco per il file immagine
    new_name = secrets.token_hex(8)
    new_file_name = new_name + file_ext

    # Percorso del file immagine nel server
    file_path = os.path.join(os.getcwd(), "myflaskblog", "static", "images", new_file_name)

    # Salva il file immagine nel server
    image_file_data.save(file_path)

    # TODO: rimuovere il vecchio file immagine (os)
    # TODO: ridurre le dimensioni del file immagine caricato (pillow)

    # Ritorna il nuovo nome del file immagine
    return new_file_name

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
