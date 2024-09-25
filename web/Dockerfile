ARG NODE_VERSION=20

FROM node:${NODE_VERSION}-alpine AS build
WORKDIR /app

COPY . .

RUN rm -rf node_modules dist .env

RUN yarn install

RUN yarn build

FROM node:${NODE_VERSION}-alpine AS production
RUN yarn global add serve
WORKDIR /app
COPY --from=build /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]