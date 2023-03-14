FROM node:19-alpine

WORKDIR /web-frontend

COPY . .

# Create environment variables
ARG API_URL
RUN sh dockerize/create-env-file.sh REACT_APP_API_URL=$API_URL

# Install dependencies
RUN npm ci

RUN npm run build

ENV NODE_ENV production

EXPOSE 3000

CMD [ "npx", "serve", "-s", "build" ]
