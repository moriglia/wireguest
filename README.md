# WireGuest
![Check Python code with Pylava](https://github.com/moriglia/wireguest/workflows/Pylava/badge.svg)

A Django web application for Wireguard key generation and management.

## WhyreGuest?
Because with WireGuest private keys are created on the client side
of the application. The server never sees the private keys. It receives
the public keys from the user.

## Usage

### Just run
```bash
python3 manage.py runserver
```

### Run with `pipenv`
```bash
# Only the first time:
pipenv install ;

# then:
pipenv run python manage.py runserver
```

### Run with make
```bash
# Only the first time:
pipenv install ;

# then:
make run
```

### Install as user service
```bash
# Pipenv environment creation and service configuration
make install ;

# start service
systemctl --user start django-wireguest ;
```

### Install as global service
```bash
# without privileges
make service ;

# as root:
cp django-wireguest.service /etc/systemd/system/ ;
systemctl daemon-reload;
systemctl enable django-wireguest ;
systemctl start django-wireguest ;
```

## Requirements
If you use `pipenv` you may need to install:
* `libsasl2-dev`
* `libldap2-dev`
