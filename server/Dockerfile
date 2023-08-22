FROM node:20.5-alpine AS build

RUN apk update && apk add --no-cache \
    shadow \
    bash \
    make \
    g++

USER node

WORKDIR /app

COPY --chown=node:node package*.json ./

RUN npm ci

COPY --chown=node:node . .

RUN npm run build

EXPOSE 3000

FROM build as local

USER root

RUN npm i -g @nestjs/cli

USER node

ENTRYPOINT ["tail", "-f", "/dev/null"]

FROM build as production

CMD ["npm", "run", "start:prod"]
