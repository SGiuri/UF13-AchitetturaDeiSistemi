#USERS

import os
import secrets
from flask import render_template, url_for, redirect, flash
from myflaskblog import app, db, bcrypt
from myflaskblog.forms import RegistrationForm, LoginForm, UpdateUserForm
from myflaskblog.forms import NewPostForm
from myflaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required


users = Blueprint('users', __name__)


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

