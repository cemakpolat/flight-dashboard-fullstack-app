# Flight Visualization App

This is a simple flight visualization app built with React and Vite. It uses the HiveMQ MQTT broker to connect to the flight data.

## Running the app

1. Clone the repository
2. Run `npm install` to install the dependencies
3. Run `npm run dev` to start the development server

## Running the app in Docker

1. Run `docker compose up --build` to start the Docker container
2. Run `docker compose down` to stop the Docker container

## Running the app in Docker with environment variables

1. Run `docker compose up --build` to start the Docker container

Sure! Here's a short explanation of your approach:  

**📌 Static Environment Variable Injection in React (Build Time Approach)**  

In this setup, we pass `REACT_APP_MQTT_BROKER` **at build time** so that it becomes part of the React static files. This ensures a stable and predictable configuration without runtime modifications.  

### **How It Works?**  
1. **Pass the variable during the build** using `docker-compose.yml`:  
   ```yaml
   args:
     REACT_APP_MQTT_BROKER: "ws://broker.emqx.io:8083/mqtt"
   ```
2. **Inject the variable inside `env.js` during the build stage in `Dockerfile`**:  
   ```dockerfile
   ARG REACT_APP_MQTT_BROKER
   RUN echo "window._env_ = { REACT_APP_MQTT_BROKER: \"$REACT_APP_MQTT_BROKER\" };" > /usr/share/nginx/html/env.js
   ```
3. **React reads `env.js` statically at runtime**:  
   ```javascript
   const host = window._env_?.REACT_APP_MQTT_BROKER || 'ws://backup-broker.example.com:8083/mqtt';
   ```
