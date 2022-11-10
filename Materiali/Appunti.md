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
* WSGI (Web Server Gateway Interface)
Per eseguire un'applicazione Flask visibile da browser devo avviare il server.
```commandline
flask run
```
  * Werkzeug 
  * GUnicorrn NGINX
********
# Lezione 2 - 16/11/22
* HTML + CSS: Bootstrap
* Jinja2
********
# Lezione 3 - 07/12/23
* Moduli
* Database
********
# Lezione 4 - 14/12/23
* Login Manager
********
# Lezione 5 - 21/12/23

********
# Lezione 6 - 01/02/23
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

