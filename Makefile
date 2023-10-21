COMPOSE=${ARGS} docker-compose

install: base-install server-install web-install

base-install:
	if [ ! -f .env ]; then cp .env.example .env; fi
	${COMPOSE} up -d --force-recreate --build

server-install:
	${COMPOSE} exec server npm install

web-install:
	${COMPOSE} exec web npm install

start: base-start
	trap 'make running-services-kill' SIGINT; \
	(${MAKE} server-start & ${MAKE} web-start & ${MAKE} client-start & wait)

base-start:
	${COMPOSE} up -d

server-start:
	${COMPOSE} exec -T server npm run start:dev

web-start:
	${COMPOSE} exec -T web npm run dev

client-start:
	${COMPOSE} exec -T client watchexec -r -e py poetry run python src/main.py

running-services-kill: server-kill web-kill client-kill

server-kill:
	${COMPOSE} exec server pkill -f "node" || true

web-kill:
	${COMPOSE} exec web pkill -f "node" || true

client-kill:
	${COMPOSE} exec client pkill -f "watchexec" || true

down:
	${COMPOSE} down

lint: server-lint web-lint

server-lint:
	${COMPOSE} exec server npm run lint

web-lint:
	${COMPOSE} exec web npm run lint
	${COMPOSE} exec web npm run type-check

format: server-format web-format

server-format:
	${COMPOSE} exec server npm run format

web-format:
	${COMPOSE} exec web npm run format
