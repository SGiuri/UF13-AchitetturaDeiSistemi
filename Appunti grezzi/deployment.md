https://www.linode.com/lp/free-credit-short/?promo=sitelin100-02162023&promo_value=100&promo_length=60&utm_source=google&utm_medium=cpc&utm_campaign=11178784771_109179230323&utm_term=g_kwd-2629795801_e_linode&utm_content=466940520440&locationid=9050650&device=c_c&gclid=EAIaIQobChMI0OjFlYCR_gIVKYxoCR0qUg-lEAAYASAAEgJUp_D_BwE




Password: testPasswordSecured23


************SETUP

simone@LOCAL_MACHINE$ ssh root@139.162.183.36

root@localhost:~# apt update && apt upgrade

impostiamo un hostname:
root@localhost:~# hostnamectl set-hostname my-server
root@localhost:~# hostname
my-server

salviamo l'hostname appena creato sul fle hosts:
root@localhost:~# nano /etc/hosts
ctrl x, y, enter

Creaimo un user non onnipotente
root@localhost:~# adduser simone

aggiungiamo questo user al gruppo sudo in modo che possa eseguire comndi da amministratore

root@localhost:~# adduser simone sudo

eseguiamo il log out e il log in con il nuovo id
root@localhost:~# exit

simone@LOCAL_MACHINE$ ssh simone@139.162.183.36

da questo momento il prompt sara':

simone@my-server:~#

Creiamo ora una coppi di chiavi ssh per fare un accesso alla macchina remota senza password

Lavoriamo ora in parallelo 
su macchina locale simone@LOCAL_MACHINE:~$
e
su server: simone@my-server:~$

Sulla macchina loale creiamo una coppia di chiavi ssh:

simone@LOCAL_MACHINE:~$ ssh-keygen -b 4096
questo comando crea due file: id_rsa e id_rsa.pub
Il secondo file e' la chiave pubblica e va spostata sul server
Cpiamolo sul nostro server:

simone@LOCAL_MACHINE:~$ scp ~/.ssh/id_rsa.pub simone@139.162.183.36:~/.ssh/authorized_keys

Ora sul server c'e' uan copia del file id_rsa.pub con nuovo nome: authorized_keys
Questo file e questa cartella ora dovranno essere accessibili in scrittura e lettura dal proprietario del file:
simone@my-server:~$ sudo chmod 700 ~/.ssh/
simone@my-server:~$ sudo chmod 600 ~/.ssh/*

per controllare lo stato dei permessi si puo' usare: 
simone@my-server:~$ ls -ltr ~/.ssh/

Ora posso modificare la possibilita' di accedere al server usando una password modificando il file sshd_config in modo da evitare l'accesso al server con metodi di bruteforse
simone@my-server:~$ sudo nano /etc/ssh/ssh_config
   
 	PasswordAuthentication no

Facciamo ripartire il server ssh
simone@my-server:~$ sudo systemctl restart ssh

Installiamo un firewall (ufw, uncmplicated firewall):
simone@my-server:~$ sudo apt install ufw
					sudo ufw default allow outgoing
					sudo ufw default deny incoming
					sudo ufw allow ssh
					sudo ufw allow 5000
					sudo ufw enable
					sudo ufw status

Ora possiamo spostare l'applicazione sul server.
*************
DEPLOYMENT:
Creiamo un pipfreeze:
(myflaskblog) C:\Users\simon....\: pip list --format=freeze > requirements.txt

Verifico che il file sia nella cartella del progetto che copio sulla versione locale di linux, in /home/simone

simone@LOCAL_MACHINE: scp -r /home/simone/Lezione8/myFlaskBlog/ simone@139.162.183.36:~/


Istallazione di Python sul Server
`sudo apt install python3-pip` 
`sudo apt install python3-venv`
`python3 -m venv myFlaskBlog/venv`

Creiamo un venv, lo attiviamo e installiamo i requirements
 `source venv/bin/activate` - in our Flask_Blog dir we activate our venv
 `pip install -r requirements.txt` - we install our pip packages into our venv
`sudo touch /etc/config.json` &
`sudo nano /etc/config.json` - where we now store our environment variables inside a file instead of the system 
`sudo nano flaskblog/config.py` - add the following code 
`import json`
`with open('/etc/config.json') as config_file:
config = json.load(config_file)`
we are still in config.py and replace `os.environ.get` with `config.get`
`export FLASK_APP=run.py` - where we assign the environment variable FLASK_APP to the module
`flask run --host=0.0.0.0` -  we run a local dev server on the linode
`sudo apt install nginx`
`pip install gunicorn`
`sudo rm /etc/nginx/sites-enabled/default` - we remove nginx default config
`sudo nano /etc/nginx/sites-enabled/flaskblog` -  new nginx config solely for our app. Add the code from Corey's snippets. Remember: gunicorn is running on port 8000, nginx is running on port 80

server {
    listen 80;
    server_name YOUR_IP_OR_DOMAIN;

    location /static {
        alias /home/YOUR_USER/YOUR_PROJECT/flaskblog/static;
    }

    location / {
        proxy_pass http://localhost:8000;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}

`sudo nano ufw allow http/tcp` &
`sudo ufw delete allow 5000` &
`sudo ufw enable` 
`sudo systemctl restart nginx` - restart nginx server
access your URL/static/main.css. This proves that nginx server is serving static content and that it cannot serve the dynamic content because Gunicorn is not running yet.
`nproc --all` - to find out how many cores on this machine
`gunicorn -w 3 run:app` - now that gunicorn is running, we access our main site and this proves that nginx is passing HTTP requests to gunicorn
`sudo apt install supervisor` - this software (written in python!) will run Gunicorn in the background
`sudo nano /etc/supervisor/conf.d/flaskblog.conf` - create a supervisor config file referring to flaskblog package, and Gunicorn. Add corey's snippets
- note that we point supervisor to (yet uncreated) log files located:
`/var/log/flaskblog/flaskblog.err.log` &
`/var/log/flaskblog/flaskblog.out.log`

[program:flaskblog]
directory=/home/YOUR_USER/YOUR_PROJECT
command=/home/YOUR_USER/YOUR_PROJECT/venv/bin/gunicorn -w 3 run:app
user=YOUR_USER
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/flaskblog/flaskblog.err.log
stdout_logfile=/var/log/flaskblog/flaskblog.out.log

`sudo mkdir -p /var/log/flaskblog` 
`sudo touch /var/log/flaskblog/flaskblog.err.log` &
`sudo touch /var/log/flaskblog/flaskblog.out.log` - where we now create our log files
`sudo supervisorctl reload` - where we restart supervisor
`sudo nano /etc/nginx/nginx.conf` - where we access general config file for nginx
`client_max_body_size 5M;` - add this code in the config file to increase upload limit from 2MB to 5MB
`sudo systemctl restart nginx`