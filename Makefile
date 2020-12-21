LOG_FILE ?= wireguest.log
ERR_FILE ?= wireguest.err
PIPE_OPT ?= 1>> $(LOG_FILE) 2>> $(ERR_FILE)
MANAGE = pipenv run python manage.py
WIREGUEST_WD ?= `pwd`
SERVICE_NAME ?= django-wireguest
USER_SERVICE_UNITS ?= $(HOME)/.config/systemd/user

CONFIGURATION_HEADERS ?= test
CONFIGURABLE_FILES = keygenerator/wireguard_config.py wireguest/ldap_settings.py

.PHONY: run migrations pylava install uninstall clean service openshell test coverage config

run:
	$(MANAGE) runserver $(PIPE_OPT)

%.service: %.service.template
	cpp -P -DWIREGUEST_WD=$(WIREGUEST_WD) $< -o $@

service: $(SERVICE_NAME).service

clean:
	rm -rf $(SERVICE_NAME).service $(LOG_FILE) $(ERR_FILE) $(CONFIGURABLE_FILES)

# See config_headers/README.md for more information
%.py: %.py.cpp
	cpp -P -nostdinc -I config_headers/$(CONFIGURATION_HEADERS) $< -o $@

config: $(CONFIGURABLE_FILES)

install: $(SERVICE_NAME).service
	pipenv install ;
	mkdir -p $(USER_SERVICE_UNITS) ;
	cp $< $(USER_SERVICE_UNITS)/ ;

uninstall:
	rm -rf $(USER_SERVICE_UNITS)/$(SERVICE_NAME).service

pylava:
	pipenv run pylava

test: config
	$(MANAGE) test

coverage: config
	# Configuration is saved in .coveragerc
	pipenv run coverage run manage.py test
	pipenv run coverage html

migrations: config
	$(MANAGE) makemigrations ;
	$(MANAGE) migrate ;

openshell:
	$(MANAGE) shell ;
