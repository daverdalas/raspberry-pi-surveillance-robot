FROM core:latest AS core

FROM node:20.5-alpine AS build

RUN apk update && apk add --no-cache \
    shadow \
    bash \
    make \
    g++

USER node

ARG VITE_STREAM_URL
ARG VITE_NEXT_MESSAGE_MAX_WAIT_TIME
ARG VITE_WEBSOCKET_URL

WORKDIR /app

COPY --chown=node:node package*.json ./

RUN npm ci

COPY --chown=node:node --from=core ./ /core

COPY --chown=node:node . .

RUN npm run build

FROM build as local

EXPOSE 5173

ENTRYPOINT ["tail", "-f", "/dev/null"]

FROM nginx:stable-alpine3.17 AS production

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
