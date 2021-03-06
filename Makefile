LOG_FILE ?= wireguest.log
ERR_FILE ?= wireguest.err
PIPE_OPT ?= 1>> $(LOG_FILE) 2>> $(ERR_FILE)

MANAGE = pipenv run python manage.py

WIREGUEST_WD ?= `pwd`
SERVICE_NAME ?= django-wireguest
USER_SERVICE_UNITS ?= $(HOME)/.config/systemd/user

CONFIGURATION_HEADERS ?= test
CONFIGURABLE_FILES = $(subst .cpp.,.,$(shell find . -name "*.cpp.*"))

COVERAGE_FORMAT ?= xml # Set it to html to generate htmlcov/ folder

.PHONY: run migrations pylava install uninstall clean service openshell test coverage config

run:
	$(MANAGE) runserver $(PIPE_OPT)

%.service: %.service.template
	cpp -P -DWIREGUEST_WD=$(WIREGUEST_WD) $< -o $@

service: $(SERVICE_NAME).service

clean:
	rm -rf $(SERVICE_NAME).service $(LOG_FILE) $(ERR_FILE) $(CONFIGURABLE_FILES)

# See config_headers/README.md for more information about the configuration headers
# The following receipe is used for both python and js files
PREPROCESS = cpp -P -nostdinc -I config_headers/$(CONFIGURATION_HEADERS) $< -o $@

%.py: %.cpp.py
	$(PREPROCESS)

%.js: %.cpp.js
	$(PREPROCESS)

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
	pipenv run coverage $(COVERAGE_FORMAT)

migrations: config
	$(MANAGE) makemigrations ;
	$(MANAGE) migrate ;

openshell:
	$(MANAGE) shell ;
