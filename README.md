# FSND-P5 Linux Server Configuration:

Live at 52.24.181.212 and ec2-52-24-181-212.us-west-2.compute.amazonaws.com/

### Steps to setup FSND-P3 on a Ubuntu server
#### 1. Download RSA Key, restrict key access, and ssh into instance:
 -  `mv ~/Downloads/udacity_key.rsa ~/.ssh/`
 -  `chmod 600 ~/.ssh/udacity_key.rsa`
 -  `ssh -i ~/.ssh/udacity_key.rsa root@52.26.58.234`

#### 2. Install & upgrade packages, git
 -  `apt-get update`
 - `sudo apt-get upgrade`
 - `apt-get install unattended-upgrades`
 - `dpkg-reconfigure -plow unattended-upgrades`
 - `apt-get install git`
 - `git config --global user.name "Kirk Brunson"`
 - `git config --global user.email "kirkbrunson314@gmail.com"`

#### 3. Install & configure apache
 - `apt-get install apache2`
 - `apt-get install python-setuptools libapache2-mod-wsgi`
 - `echo "ServerName HOSTNAME" | sudo tee /etc/apache2/conf-available/fqdn.conf`
 - `a2enconf fqdn`
 - `apt-get install libapache2-mod-wsgi python-dev`
 - `a2enmod wsgi`
 - `service apache2 restart`

#### 4. Clone & configure FSND-P3
 - `cd /var/www/`
 - `mkdir app`
 - `cd app`
 - `touch .htaccess | echo "RedirectMatch 404 /\.git" >> .htaccess`
 - `mkdir app`
 - `cd app`
 - `git clone https://github.com/kirkbrunson/FSND-P5.git`
 - `cd FSND-P5`
 - `rm README.md`
 - `mv project.py __init__.py`
 - `mv * ..`
 - `cd ..`
 - `rm -rf FSND-P5`

#### 5. Install python packages
 - `apt-get install python-pip`
 - `pip install virtualenv`
 - `virtualenv venv` 
 - `chmod -R 777 venv`
 - `pip install Flask-Seasurf`
 - `pip install requests`
 - `pip install --upgrade oauth2client`
 - `pip install sqlalchemy`
 - `apt-get install python-psycopg2`
 - `pip install bleach`

#### 6. More apache config
  ```touch /etc/apache2/sites-available/app.conf | echo 
  "<VirtualHost *:80>
	      ServerName 52.24.181.212
	      ServerAdmin admin@52.24.181.212
	      ServerAlias ec2-52-24-181-252.us-west-2.compute.amazonaws.com
	      WSGIScriptAlias / /var/www/app/app.wsgi
	      <Directory /var/www/app/app/>
	          Order allow,deny
	          Allow from all
	      </Directory>
	      Alias /static /var/www/app/app/static
	      <Directory /var/www/app/app/static/>
	          Order allow,deny
	          Allow from all
	      </Directory>
	      ErrorLog ${APACHE_LOG_DIR}/error.log
	      LogLevel warn
      CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>" >> 
/etc/apache2/sites-available/app.conf```
 - `a2ensite app`
 - `cd ..` 
 ```touch app.wsgi | echo '#!/usr/bin/python
 import sys
 import logging
 logging.basicConfig(stream=sys.stderr)
 sys.path.insert(0,"/var/www/app/")
 
 from app import app as application
 application.secret_key = "Add your secret key"' >> app.wsgi```
- `service apache2 restart`

#### 7. Install & config postgres & instantiate db
 - `apt-get install postgresql postgresql-contrib`
 - `cd /etc/postgresql/9.3/main/`
 - `su - postgres`
 - `echo "CREATE USER catalog WITH PASSWORD 'catalogpw';" | psql`
 - `echo "ALTER USER catalog CREATEDB;" | psql`
 - `echo "CREATE DATABASE appdb WITH OWNER catalog;" | psql`
 - `echo "REVOKE ALL ON SCHEMA public FROM public;" | psql`
 - `echo "GRANT ALL ON SCHEMA public TO catalog;" | psql`
 - `exit`
 - `cd /var/www/app/app/`
 **Note: Refactored __init__.py, database_setup.py & createDB.py for postgres compatibility.**
 - `python database_setup.py`
 - `python createDB.py`

#### 8. NTP config
 - `dpkg-reconfigure tzdata`
 - `apt-get install ntp`
 - `vim /etc/ntp.conf` (edited to proper ntp server pool)

#### 9. Monitor & ban abuse
 - `apt-get install python-pip build-essential python-dev`
 - `pip install Glances`
 - `apt-get install lm-sensors`
 - `pip install PySensors`
 - `apt-get install fail2ban`
 - `cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local`
 - `vim /etc/fail2ban/jail.local`
  - set bantime  = 900
  - destemail = grader@localhost
 - `apt-get install sendmail iptables-persistent`
 - `service fail2ban restart`

#### 10. Add User
 -  `adduser grader`
 -  `visudo` ( add "grader ALL=(ALL:ALL) ALL" under line "root ALL ..." )
 
#### 11. SSH
 - `vim /etc/ssh/sshd_config` (Enable password login)
 - On local machine: `ssh-keygen`
 - `scp ~/.ssh/id_rsa.pub grader@52.24.181.212:`
 - Back on root session: `su - grader`
 - `mkdir ~/.ssh`
 - `chmod 700 ~/.ssh`
 - `cat ~/id_rsa.pub >> ~/.ssh/authorized_keys`
 - `rm ~/id_rsa.pub`
 - `chmod 600 ~/.ssh/authorized_keys`
 - `exit`
 - `vim /etc/ssh/sshd_config` (Change ssh to 2200, Enforce ssh key login, Don't permit root login)
 - `service ssh restart`

#### 12. Firewall config
 - `ufw enable`
 - `ufw allow 2200/tcp`
 - `ufw allow 80/tcp`
 - `ufw allow 123/udp`
 - `service ufw restart`
 - `exit` (Log out of root)