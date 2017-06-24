get-latest-static-data:
	curl -o google_transit.zip http://web.mta.info/developers/data/nyct/subway/google_transit.zip
	unzip -o -d google_transit google_transit.zip

generate_schedule:
	python lib.py

build:
	docker build -t static-mta .

run:
	docker run -it -p 5000:5000 static-mta ./app.py

dev:
	docker run -it static-mta /bin/sh
