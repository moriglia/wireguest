LOG_FILE ?= wireguest.log
ERR_FILE ?= wireguest.err
PIPE_OPT ?= 1>> $(LOG_FILE) 2>> $(ERR_FILE)
MANAGE = pipenv run python manage.py
WIREGUEST_WD ?= `pwd`
SERVICE_NAME ?= django-wireguest
USER_SERVICE_UNITS ?= $(HOME)/.config/systemd/user

.PHONY: run

run:
	$(MANAGE) runserver $(PIPE_OPT)

%.service: %.service.template
	cpp -P -DWIREGUEST_WD=$(WIREGUEST_WD) $< -o $@

service: $(SERVICE_NAME).service

clean:
	rm -rf $(SERVICE_NAME).service $(LOG_FILE) $(ERR_FILE)

install: $(SERVICE_NAME).service
	pipenv install ;
	mkdir -p $(USER_SERVICE_UNITS) ;
	cp $< $(USER_SERVICE_UNITS)/ ;

uninstall:
	rm -rf $(USER_SERVICE_UNITS)/$(SERVICE_NAME).service