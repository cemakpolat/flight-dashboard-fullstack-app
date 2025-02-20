import random
import time
import json
import logging
import paho.mqtt.client as mqtt
from paho.mqtt import MQTTException
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# MQTT Broker details - Read from environment variables
MQTT_BROKER = os.environ.get("MQTT_BROKER", "broker.emqx.io")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))  # Default to 1883 if not found
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "flights/topic")
MESSAGE_SENDING_INTERVAL = int(os.environ.get("MESSAGE_SENDING_INTERVAL", 10)) # Default to 10 if not found


# List of cities - Extended and read from environment variables
DEFAULT_CITIES = ["NewYork", "London", "Paris", "Tokyo", "Sydney", "Dubai", "Berlin", "Rome", "Madrid", "Toronto", "LosAngeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "SanAntonio", "SanDiego", "Dallas", "SanJose", "Austin"]
CITIES_ENV = os.environ.get("CITIES")

if CITIES_ENV:
    CITIES = [city.strip() for city in CITIES_ENV.split(",")]  # Split comma-separated string
else:
    CITIES = DEFAULT_CITIES  # Use the default list if the environment variable is not set


def publish_data(client, data, mqtt_topic):
    """Publishes the flight data to the MQTT broker."""
    try:
        json_data = json.dumps(data)
        result = client.publish(mqtt_topic, json_data)
        status = result[0]
        if status == 0:
            logging.info(f"Sent `{json_data}` to topic `{mqtt_topic}`")
        else:
            logging.error(f"Failed to send message to topic {mqtt_topic}. Result code: {status}")
    except Exception as e:
        logging.error(f"Error publishing data: {e}")


def generate_flight_data():
    """Generates flight data with boarding status, altitude, fuel level, and potential issues."""
    flight_id = f"flight_{random.randint(100, 999)}"
    current_hub = random.choice(CITIES)
    target_hub = random.choice(CITIES)
    while target_hub == current_hub:
        target_hub = random.choice(CITIES)

    if random.random() < 0.7:
        available_hubs = [city for city in CITIES if city not in {target_hub, current_hub}]
        transition_hub = random.choice(available_hubs)
    else:
        transition_hub = None

    boarding_complete = bool(random.randint(0, 1))
    altitude = random.randint(0, 40000)
    fuel_level = round(random.uniform(0.05, 1.0), 2)
    possible_issues = ["None", "Mechanical Failure", "Turbulence", "Medical Emergency", "Weather Delay"]
    current_issue = random.choice(possible_issues)

    # Determine status:
    status = "UNKNOWN" # Default status to avoid unassigned variable errors
    if not boarding_complete:
        status = "BOARDING"  # Still boarding
    elif altitude < 1000:
        status = "GROUNDED"  # the plane must be grounded
    elif current_issue == "Mechanical Failure" or fuel_level < 0.1:
        status = "CANCELLED"  # Flight cannot happen - priority
    elif current_issue == "Medical Emergency":
        status = "DIVERTED"  # Medical emergency takes precedence
    else:
        status = random.choice(["OK", "DELAYED"])  # default values

    data = {
        "flight_id": flight_id,
        "boarding_complete": boarding_complete,
        "altitude": altitude,
        "fuel_level": fuel_level,
        "current_issue": current_issue,
        "status": status,
        "current_hub": current_hub,
        "target_hub": target_hub,
        "transition_hub": transition_hub,
        "duration": random.randint(5, 15),
    }
    return data


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logging.info("Connected to MQTT Broker!")
    else:
        logging.error(f"Failed to connect, return code {rc}")


def main():
    client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
    client.on_connect = on_connect

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()  # Start the MQTT client loop in the background
        logging.info(f"Successfully connected to MQTT broker {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        logging.error(f"Error connecting to MQTT broker: {e}")
        return

    try:
        while True:
            num_flights = random.randint(1, 5)
            for _ in range(num_flights):
                flight_data = generate_flight_data()
                publish_data(client, flight_data, MQTT_TOPIC)
            time.sleep(MESSAGE_SENDING_INTERVAL)
    except MQTTException as err:
        logging.error(f"MQTT Exception occurred: {err}")
    except Exception as err:
        logging.error(f"An unknown error occurred: {err}")
    finally:
        client.loop_stop()  # Stop the MQTT loop
        client.disconnect()
        logging.info("Disconnected from MQTT broker.")


if __name__ == "__main__":
    main()