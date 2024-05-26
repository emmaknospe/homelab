FROM node:22-alpine AS build-stage
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build
# RUN npm prune --production
RUN ls -al

FROM node:22-alpine
WORKDIR /app
COPY --from=build-stage /app/build build/
COPY --from=build-stage /app/node_modules node_modules/
COPY package.json .
EXPOSE 3000
CMD [ "node", "build" ]
