# FSND-P5 Linux Server Configuration:

Site live [here][1]
IP Address & Port: 52.26.58.234:2200

### Steps to setup FSND-P3 on a Ubuntu Linux server:

1. Download RSA Key, restrict key access, and ssh into instance:
 -  mv ~/Downloads/udacity_key.rsa ~/.ssh/
 -  chmod 600 ~/.ssh/udacity_key.rsa
 -  ssh -i ~/.ssh/udacity_key.rsa root@52.26.58.234

2. Add User:
 -  adduser grader
 -  visudo > add "grader ALL=(ALL:ALL) ALL" under root

3. Update packages:
 -  sudo apt-get update
 -  sudo sudo apt-get upgrade
 -  sudo apt-get install unattended-upgrades
 -  sudo dpkg-reconfigure -plow unattended-upgrades

4. Configure Ports & UFW:
 - 	sudo vim /etc/ssh/sshd_config > 
 -  Port 2200, PermitRootLogin No, UseDNS no, AllowUsers grader
 -  sudo ufw enable
 -  sudo ufw allow 2200/tcp
 -  sudo ufw allow 80/tcp
 -  sudo ufw allow 123/udp

5. Configure system time:
 -  sudo dpkg-reconfigure tzdata
 -  sudo apt-get install ntp
 -  sudo vim /etc/ntp.conf (Edit ntp servers)

6. Install & Configure Apache
 -  sudo apt-get install apache2
 -  sudo apt-get install python-setuptools libapache2-mod-wsgi
 -  echo "ServerName HOSTNAME" | sudo tee /etc/apache2/conf-available/fqdn.conf
 -  sudo a2enconf fqdn
 -  sudo apache2 reload
 -  sudo apt-get install libapache2-mod-wsgi python-dev
 -  sudo a2enmod wsgi
 -  sudo service apache2 restart
 -  create app dir and cd to it -> /var/www/app/app/


7. Install Git, clone repo, and config app
 -  sudo apt-get install git
 -  git config --global user.name "My name"
 -  git config --global user.email "myemail@domain.com"
 -  git clone https://github.com/kirkbrunson/FSND-P3.git
 -  cd FSND-P3
 -  mv * ..
 -  cd ..
 -  rm -rf FSND-P3
 -  Refactor for apache compatability
 -  mv project.py __init__.py
 -  cd ..
 -  sudo vim .htaccess > RedirectMatch 404 /\.git
 -  cd app
 -  sudo apt-get install python-pip
 -  sudo pip install virtualenv
 -  sudo virtualenv venv
 -  sudo chmod -R 777 venv
 -  sudo pip install Flask
 -  sudo pip install Flask-Login
 -  sudo pip install Flask-Seasurf
 -  sudo pip install httplib2
 -  sudo pip install requests
 -  sudo pip install --upgrade oauth2client
 -  sudo pip install sqlalchemy
 -  sudo apt-get install python-psycopg2
 -  sudo pip install bleach
 -  add VirtualHost file 
 -  sudo nano /etc/apache2/sites-available/app.conf
 -  sudo a2ensite app
 -  cd .. 
 -  sudo vim app.wsgi (import app from)
 -  sudo service apache2 restart

8. Install & setup postgresDB
 -  sudo apt-get install postgresql postgresql-contrib
 -  cd /etc/postgresql/9.3/main/
 -  sudo vim pg_hba.conf (confirm remote connection disabled)
 -  su - postgres
.. psql
 -  CREATE USER catalog WITH PASSWORD 'YOURPSWD';
 -  ALTER USER catalog CREATEDB;
 -  CREATE DATABASE appdb WITH OWNER catalog;
 -  REVOKE ALL ON SCHEMA public FROM public;
 -  GRANT ALL ON SCHEMA public TO catalog;
 -  \q
 -  exit
 -  cd /var/www/app/app/
 -  Refactor db files database_setup.py, createDB.py & __init__.py for postgres
 -  python database_setup.py
 -  python createDB.py

9. Monitoring:
 - sudo apt-get install python-pip build-essential python-dev
 - sudo pip install Glances
 - sudo apt-get install lm-sensors
 - sudo pip install PySensors



[1]: http://ec2-52-26-58-234.us-west-2.compute.amazonaws.com/
