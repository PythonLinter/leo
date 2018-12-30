
leo deployment guide for fist time
==================================

Preparation
-----------

### Prerequicites:

```bash
sudo apt-get install build-essential python3-pip postgresql libpq-dev
```

### Virtual env

```bash
sudo pip3 install -U pip setuptools wheel
sudo pip3 install virtualenvwrapper
``` 

##### Create and login as `dev` user

```bash
sudo adduser dev
su - dev
mkdir ~/workspace
echo "export VIRTUALENVWRAPPER_PYTHON=`which python3.6`" >> ~/.bashrc
echo "alias v.activate=\"source $(which virtualenvwrapper.sh)\"" >> ~/.bashrc
source ~/.bashrc
v.activate
mkvirtualenv --python=$(which python3.6) --no-site-packages leo

```

##### Setup Database

```bash
echo 'CREATE USER dev' | sudo -u postgres psql
echo 'CREATE DATABASE leo' | sudo -u postgres psql
echo 'GRANT ALL PRIVILEGES ON DATABASE leo TO dev' | sudo -u postgres psql
echo "ALTER USER dev WITH PASSWORD 'password'" | sudo -u postgres psql
```

##### Config file

Create a file `/etc/nuemd-coder/leo.yml` with this contents:

```yaml
db:
  uri: postgresql://dev:password@localhost/leo
  echo: false

messaging:
  default_messenger: restfulpy.messaging.SmtpProvider

smtp:
  host: mail.carrene.com
  port: 587
  username: nc@carrene.com
  password: <smtp-password>
  local_hostname: carrene.com

logging:

  handlers:
    main:
      filename: /var/log/leo/leo.log
      
    error:
      filename: /var/log/leo/error.log
    
    worker:
      filename: /var/log/leo/worker.log
    
  loggers:
    worker:
      handlers: [worker, error]
```

### Install

```bash
su - dev
cd ~/workspace/leo
v.activate && workon leo
pip install -e .
```

##### Database objects

```bash
v.activate && workon leo
leo admin setup-db
leo admin base-data
leo admin mockup-data  #  if desirable
```

##### wsgi

/etc/nuemd-coder/leo_wsgi.py
```python
from leo import leo

leo.configure(files='/etc/nuemd-coder/leo.yml')
leo.initialize_models()
app = leo

```

##### Systemd

/etc/systemd/system/leo.service:

```ini
[Unit]
Description=leo API daemon
Requires=leo.socket
After=network.target
BindsTo=leo-email-delivery.service

[Service]
PIDFile=/run/leo/pid
User=dev
Group=dev
WorkingDirectory=/home/dev/workspace/leo/
ExecStart=/home/dev/.virtualenvs/leo/bin/gunicorn --pid /run/leo/pid --chdir /etc/nuemd-coder leo_wsgi:app
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target


```

/etc/systemd/system/leo-email-delivery.service:

```ini
[Unit]
Description=leo Email delivery worker daemon
After=network.target
BindsTo=leo.service

[Service]
PIDFile=/run/leo/email-delivery-pid
User=dev
Group=dev
WorkingDirectory=/home/dev/workspace/leo/
ExecStartPre=/home/dev/.virtualenvs/leo/bin/leo -c /etc/nuemd-coder/leo.yml worker cleanup
ExecStart=/home/dev/.virtualenvs/leo/bin/leo -c /etc/nuemd-coder/leo.yml worker start
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target

```

/etc/systemd/system/leo.socket:

```ini
[Unit]
Description=leo socket

[Socket]
ListenStream=/run/leo.socket
#ListenStream=0.0.0.0:9000
#ListenStream=[::]:8000

[Install]
WantedBy=sockets.target
```

/usr/lib/tmpfiles.d/leo.conf:

```
d /run/leo 0755 dev dev -
```

Next enable the services so they autostart at boot:

```bash
systemd-tmpfiles --create
systemctl daemon-reload
systemctl enable leo.socket
```

Either reboot, or start the services manually:

```bash
systemctl start leo.socket
```

### NGINX

/etc/nginx/sites-available/nc.carrene.com

```
upstream leo_webapi {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response
    server unix:/var/run/leo.socket fail_timeout=0;
}

server {
    listen 80;

    server_name nc.carrene.com;

    root /home/dev/workspace/otter;
    index index.html;

    location / {
        try_files $uri $uri/ @rewrites;
    }

    location @rewrites {
      rewrite ^(.+)$ /index.html last;
    }


    location /apiv1/ {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      # enable this if and only if you use HTTPS
      # proxy_set_header X-Forwarded-Proto https;
      #proxy_set_header Host $http_host;
      # we don't want nginx trying to do something clever with
      # redirects, we set the Host: header above already.
      proxy_redirect off;
      proxy_pass http://leo_webapi;
    }
}

```

```bash
ln -s /etc/nginx/sites-available/nightly-nc.carrene.com /etc/nginx/sites-enabled/
```



Future Deploys
==============

#### First you connect to server with root

```bash
ssh root@carrene-new
```

After that we stop our service with this command:

```bash
service leo stop
```

#### Second you connect to server with dev user

```bash
ssh carrene-new
```

```bash
cd workspace/leo
```

```bash
git pull origin v1.0
```


#### Third you connect to server again with root

start new service with this command:

```bash
service leo start
```

#### <b style='color:red'>ATTENTION:</b> you must exit from root session
