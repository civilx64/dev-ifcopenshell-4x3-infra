none: start

build:
	docker compose -f docker-compose.yml up -d

start:
	docker run -it dev-ifcopenshell-4x3-infra

stop:
	docker compose down

clean:
	docker compose down
	docker image prune --force

rebuild: clean
	docker compose build --no-cache