import mqtt from "mqtt";
import { REACT_APP_MQTT_BROKER } from '../../public/env.js'; 

const clientId = "flightradar_" + Math.random().toString(16).substring(2, 8);
const host = window._env_?.REACT_APP_MQTT_BROKER || 'ws://backup-broker.example.com:8083/mqtt';
console.log("Using MQTT Broker:", host);


const topic = 'flights/topic';
const options = {
  keepalive: 60,
  clientId: clientId,
  protocolId: 'MQTT',
  protocolVersion: 4,
  clean: true,
  reconnectPeriod: 1000,
  connectTimeout: 5000,
};

const mqttClient = mqtt.connect(host, options);

mqttClient.on('connect', () => {
  console.log(`Client connected: ${clientId}`);
  console.log("Attempting to subscribe..."); // Add this log  
});

// TODO: This approach should not be working, but it is.
mqttClient.subscribe(topic, { qos: 0 }, (err) => {
    if (err) {
    console.error("Subscribe error:", err);
    } else {
    console.log("Subscribed to flights/topic");
    }
});
  
mqttClient.on('error', (err) => {
  console.error('Connection error: ', err);
  client.end();
});

mqttClient.on('reconnect', () => {
  console.log('Reconnecting...');
});

mqttClient.on('message', (topic, message) => {
  console.log(`Received message on topic ${topic}: ${message.toString()}`);
});

mqttClient.on('close', () => {
  console.log('Connection closed');
});

mqttClient.on('disconnect', () => {
  console.log('Disconnected');
});

export default mqttClient;