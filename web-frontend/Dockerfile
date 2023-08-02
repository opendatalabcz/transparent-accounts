FROM node:19-alpine

WORKDIR /web-frontend

COPY . .

# Set environment variables
ARG API_URL
ENV REACT_APP_API_URL=${API_URL}

# Install dependencies
RUN npm ci

RUN npm run build

ENV NODE_ENV production

EXPOSE 3000

CMD [ "npx", "serve", "-s", "build" ]
