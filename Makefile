.PHONY: deploy

brightnessMonitor:
	arduino --upload BrightnessMonitor/BrightnessMonitor.ino --board arduino:avr:diecimila --port /dev/ttyUSB0

brightnessMonitor-console:
	miniterm.py /dev/ttyUSB0

build:
	$(MAKE) build -C frontend/
	$(MAKE) build -C mta-service-status/
	$(MAKE) build -C mta-static/
	$(MAKE) build -C weather/

deploy:
	./deploy/deploy.sh

reload-services:
	./deploy/reload-services.sh
