none: start

build:
	docker build . -t dev-ifcopenshell-4x3-infra

compose:
	docker compose -f docker-compose.yml up -d

start:
	docker run -it \
		-v $(PWD):/app \
		-v $(HOME)/src/IFC-Rail-Unit-Test-Reference-Code:/root/src/IFC-Rail-Unit-Test-Reference-Code/ \
		dev-ifcopenshell-4x3-infra

stop:
	docker compose down

clean:
	docker compose down
	docker image prune --force

rebuild: clean
	docker build . --no-cache -t dev-ifcopenshell-4x3-infra