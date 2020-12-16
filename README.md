# WireGuest
![Check Python code with Pylava](https://github.com/moriglia/wireguest/workflows/Pylava/badge.svg)
![Unittest](https://github.com/moriglia/wireguest/workflows/Unittest/badge.svg)
[![codecov](https://codecov.io/gh/moriglia/wireguest/branch/master/graph/badge.svg)](https://codecov.io/gh/moriglia/wireguest)
[![GitHub license](https://img.shields.io/github/license/moriglia/wireguest)](https://github.com/moriglia/wireguest/blob/master/LICENSE)

A Django web application for Wireguard key generation and management.

## WhyreGuest?
Because with WireGuest private keys are created on the client side
of the application. The server never sees the private keys. It receives
the public keys from the user.

## Usage

In all the following methods substitute
`make config` with `make CONFIGURATION_HEADERS=production config`
after reading `config_headers/README.md` when working
with a custom configuration

### Just run
```bash
# Only the first time:
make config ;

# then:
python3 manage.py runserver
```

### Run with `pipenv`
```bash
# Only the first time:
pipenv install ;
make config ;

# then:
pipenv run python manage.py runserver
```

### Run with make
```bash
# Only the first time:
pipenv install ;
make config ;

# then:
make run
```

### Install as user service
```bash
# Pipenv environment creation and service configuration
make config ;
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
