# UF13 – Architettura dei sistemi di elaborazione
Embedding di un modello in un'applicazione 
</b>

32 h <br>
## RISULTATO ATTESO
Acquisire competenze sui modelli dell applicazioni web
Struttura dell’UF
L'UF si articola nel seguente modulo didattico, che concorre al raggiungimento del Risultato Atteso con l'apporto degli elementi di Conoscenza e Abilità descritti nella sezione successiva.
 Embedding di un modello in un’applicazione


## FINALITA' 
 Embedding di un modello in un’applicazione Web,  creazione di servizi REST con python. Serializzare un modello di machine learning.

## CONOSCENZE

- Serializzatore di un modello di machine learning
- Framework Flask
- Delivery di un applicazione Flask: uwsgi
- Django, introduzione: framework per python

## ABILITA'
- Serializzare un modello di Machine Learning;
- Creare REST service con python con Flask;
- Configurare uwgi per il rilascio di REST service;
- Utilzzo di Django per lo sviluppi di applicazioni web: introduzione
 ********
# Lezione 1 - 09/11/22
Dal Modello alla concretezza: come rendere funzionale e fruibile un modello di ML.
- https://openai.com

## La serializzazione:
- Pickle
- Joblib
- Json
- Marshal

## Introduzione a Flask:
* Impostazione del virtual environment:
Nella predisposizione del lavoro deve essere prevista la creazione di una ambiente di lavro virtuale.
  * conda
  * virtualenv
```commandline
  # Installo virtualenv
    C:\Users\...\> pip install virtualenv
  #creo la cartella di lavoro e attivo il virtual env
    C:\Users\...\>md projectFolder
  #accedo alla cartella
    C:\Users\...\>cd projectFolder
  #creo l'ambiente virtuale in cui sara' ospitato il progetto
    C:\Users\...\projectFolder> virtualenv project_env_name
  #attivo l'ambiente di levoro
    C:\Users\...\projectFolder>.\project_env_name\Scripts\activate
  #davanti al prompt compare il nome dell'ambiente di lavoro 
    (project_env_name) C:\Users\...\projectFolder>    
  
  ```
In fase di uploading del progetto su un server remoto, per creare un file requirements.txt:
```commandline
# Creo il file requirements.txt
 C:\Users\...\projectFolder> pip freeze > requirements.txt
# Se sotto Conda:
C:\Users\...\projectFolder> pip list --format=freeze > requirements.txt 
 -------
# Sul server remoto per istallare le identiche versioni dei pacchetti:
 C:\Users\...\projectFolder> pip install -r requirements.txt
```

* Hello Flask
* Set delle variabili di ambiente
```commandline
set FLASK_APP=app.py
set DEBUG=True  /False
 ```
Per eseguire un'applicazione Flask visibile da browser devo avviare il server. In modaltà sviluppatore, 
il server di default à un server lento, e non sicuro (fatto per agevolare le procedure di debug e gli aggiornamenti). 
I server di tipo production sono server WSGI (Web Server Gateway Interface). I production server che sarà possibile 
utilizzare sono (alcuni die quali svolgonoa cnhe molte altre funzioni):
  * [Werkzeug](https://pypi.org/project/Werkzeug/)
  * [GUnicorrn](https://gunicorn.org)
  * [NGINX](https://www.nginx.com)
```commandline
flask run
```

Un minial example:
```python
# Carico dalla libreria flask l'oggetto Flask, resposnabile della gestione e del coordinamento del server
from flask import Flask

# Inizializzo l'applicazione Flask che lavora sul file con nome __name__ (cioe' il file che contiene l'applicazione stessa)
app = Flask(__name__)

# La funzione che segue, decorata con @app.route("/") visualizza al link localhost:5000/ cio' che compare dopo il return
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

********
# Lezione 2 - 16/11/22
* Jinja2
Flask integra nella gestione dei file HTML il framework Jinja2 che permette di inserire condizionali e variabili 
nell'eseguire il rendering di un template html.
Non e' conveniente utilizzare il return della funzione per contenere codice html puro. 
Si preferisce renderizzare i template scritti a parte utilizzando la funzione render_template
```python
form flask import render_template

@app.route("/")
def home():
    return render_template("home.html", variabili_da_passare_all_html)
```
Utilizzando il render_tempalte, posso costruire all'interno della cartella "templates" un file html che verra' renderizzato 
da flask, passargli delle veriabili da utilizzare nell'html, costruire logiche di funzionamento.
```html
{{ nome_variabile }}
{% if condizione %}}
<p> Eseguito se condizione vera </p>
{% else %}}
<p> Eseguito se condizione falsa </p>
{% endif %}

 ```

* HTML + CSS: Bootstrap

********
# Lezione 3 - 07/12/23
  * [Flask WTF](https://flask-wtf.readthedocs.io/en/1.0.x/)
```commandline
pip install flask-wtf
# Se richiesto utilizzare anche email-validator:
pip install email-validator
```
```python
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, Email, EqualTo
```
* Appunti: 
  * Generare e impostare una secret key per gestire la sicurezza con 
  [CSRF](https://it.wikipedia.org/wiki/Cross-site_request_forgery)
    * ```app.config['SECRET_KEY']= [...]``` [Token HEX](https://docs.python.org/3/library/secrets.html)
  * Inizializzare il form su un file apposito. Definire i capi, le etichette ecc..
  * Passare il form in fase di rendering al file html.
  * Attivare i metodi specifici per i form ``` methods=['POST', 'GET']'```
  * Impostare un feedback di risposta sul file html sfruttado i ```form.campo.errors```
  * IMmpostare un messaggio flash e visualizzarlo per un miglior feedback sul successo o insuccesso dell'operazione di
  submit del form:
    * ```flash('Login avvenuto con successo', success)```

********
# Lezione 4 - 14/12/23
   
* Database
```commandline
pip install flask-sqlalchemy
```

```python
from flask-sqlachemy import SQLAlchemy
db = SQLAlchemy(app)

class User(SQLAlchemy):
    [...]
    
with app.app_context():
    db.create_all()    
    user_1 = [...]
    db.session.add(user_1)
    db.session.commit()

    User.query.all()
    User.query.first()
    User.query.filter_by(username='simone.giuri').all()
    user = User.query.filter_by(username='simone.giuri').first()
    print(user.id)
    print(user.posts)

```
********
# Lezione 5 - 21/12/23
 
* Password Hash
```commandline
pip install flask-bcrypt
```

```python
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
#[...]
password = "password"
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
candidate = "password"
bcrypt.check_password_hash(hashed_password, candidate) #--> True or False
```

* Package restucturing:
  

        └───myFlaskBlog
            ├───myflaskblog
            │   ├───static
            │   ├───templates
            │   └───__pycache__
            └───instance

* Login Manager   
```commandline
pip install flask-login
```

```python
#__init__.py
from flask_login import LoginManager
login_manager = LoginManager(app)
#[...]
```

Il Login Manager aggiunge alcune funzionalita' ai modelli definiti nei database per la gestione delle sessioni degli 
utenti in background per noi.
Per poterne attivare le funzionalita' e' necessario far sapere al login manager dov'e' l'elendo utenti e attivare alcune 
funzinalita' sui modelli.

Il Login Manager si aspetta che la classe User contenga alcuni metodi specifici che sono:
* is_active
* is_authenticated
* is_anonimous
* get_id
UserMixin li deifinisce per noi semplicemente facendo ereditare al modello User dalla classe UserMixin
Dovra' poi essere definita la funzone user_loader che definira' l'utente in base ad una condizione contenuta nel modello.

```python
# models.py
from myflaskblog import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    pass# [...]

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))
    
```
********
# Lezione 6 - 01/02/23
* Costruzione della pagina profilo utente, importazione e salvataggio di un file
* Costruzione della pagina per scrivere e aggiornare un post
*

********
# Lezione 7 - 15/02/23
********
# Lezione 8 - 01/03/23
********
# Lezione 9 - 29/03/23
Django cenni
********
# Lezione 10 - 05/04/23
Django cenni



