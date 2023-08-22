COMPOSE=${ARGS} docker-compose

install: base-install server-install web-install

base-install:
	if [ ! -f .env ]; then cp .env.example .env; fi
	${COMPOSE} up -d --force-recreate --build

server-install:
	${COMPOSE} exec server npm install

web-install:
	${COMPOSE} exec web npm install

lint: server-lint web-lint

server-lint:
	${COMPOSE} exec server npm run lint

web-lint:
	${COMPOSE} exec web npm run lint

format: server-format web-format

server-format:
	${COMPOSE} exec server npm run format

web-format:
	${COMPOSE} exec web npm run format
