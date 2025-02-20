FROM node:20-alpine AS build
WORKDIR /app

# Install Python and build tools required by node-gyp
RUN apk add --no-cache python3 make g++ 

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the app using Nginx
FROM nginx:alpine

ARG REACT_APP_MQTT_BROKER
RUN echo "window._env_ = { REACT_APP_MQTT_BROKER: \"$REACT_APP_MQTT_BROKER\" };" > /usr/share/nginx/html/env.js
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]