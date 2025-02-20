import unittest
import json
from unittest.mock import patch
from src.flight_data_generator import generate_flight_data, publish_data, MQTT_TOPIC, on_connect, CITIES


class TestFlightDataGeneration(unittest.TestCase):
    @patch("random.randint")
    @patch("random.choice")
    @patch("random.random")
    def test_generate_flight_data(self, mock_random, mock_choice, mock_randint):
        """Test the generate_flight_data function."""
        # Simulate random values for random.random() calls
        mock_random.side_effect = [0.5, 0]
        # Simulate city choices for random.choice()
        mock_choice.side_effect = ["NewYork", "London", "Paris", "Turbulence"]
        # Simulate random integers for random.randint(), flight num, altitude, fuel_level, duration
        mock_randint.side_effect = [123, 20000, 10, 7]

        flight_data = generate_flight_data()

        # Validate deterministic fields
        self.assertEqual(flight_data["flight_id"], "flight_123")
        self.assertEqual(flight_data["current_hub"], "NewYork")
        self.assertEqual(flight_data["target_hub"], "London")
        self.assertEqual(flight_data["duration"], 7)

        # Validate type and range for random fields
        self.assertIsInstance(flight_data["boarding_complete"], bool)
        self.assertIn(flight_data["status"], ["BOARDING", "GROUNDED", "CANCELLED", "DIVERTED", "OK", "DELAYED"])
        self.assertIn(flight_data["current_issue"],
                      ["None", "Mechanical Failure", "Turbulence", "Medical Emergency", "Weather Delay"])
        self.assertGreaterEqual(flight_data["altitude"], 0)
        self.assertLessEqual(flight_data["altitude"], 40000)
        self.assertGreaterEqual(flight_data["fuel_level"], 0.05)
        self.assertLessEqual(flight_data["fuel_level"], 1.0)
        self.assertIn(flight_data["transition_hub"], CITIES + [None])

        # Change the random so that the transition_hub returns None
        mock_random.side_effect = [0.8, 0]
        mock_choice.side_effect = ["NewYork", "London", "Turbulence"]
        self.assertIn(flight_data["current_issue"],
                      ["None", "Mechanical Failure", "Turbulence", "Medical Emergency", "Weather Delay"])

    @patch("paho.mqtt.client.Client")
    def test_publish_data_success(self, mock_client):
        """Test successful publishing of data."""
        mock_instance = mock_client.return_value
        mock_instance.publish.return_value = (0, 1)  # Simulate successful publish

        data = {"test_key": "test_value"}
        publish_data(mock_instance, data, MQTT_TOPIC)

        mock_instance.publish.assert_called_once_with(MQTT_TOPIC, json.dumps(data))

    @patch("paho.mqtt.client.Client")
    def test_publish_data_failure(self, mock_client):
        """Test failure in publishing data."""
        mock_instance = mock_client.return_value
        mock_instance.publish.return_value = (1, 1)  # Simulate failed publish

        data = {"test_key": "test_value"}
        with self.assertLogs(level="ERROR") as log:
            publish_data(mock_instance, data, MQTT_TOPIC)

        self.assertIn("Failed to send message to topic", log.output[0])

    @patch("paho.mqtt.client.Client")
    def test_on_connect_success(self, mock_client):
        """Test successful connection to MQTT broker."""
        mock_instance = mock_client.return_value
        with self.assertLogs(level="INFO") as log:
            on_connect(mock_instance, None, None, 0)
            self.assertIn("Connected to MQTT Broker!", log.output[0])

    @patch("paho.mqtt.client.Client")
    def test_on_connect_failure(self, mock_client):
        """Test failed connection to MQTT broker."""
        mock_instance = mock_client.return_value
        with self.assertLogs(level="ERROR") as log:
            on_connect(mock_instance, None, None, 1)
            self.assertIn("Failed to connect, return code 1", log.output[0])


if __name__ == "__main__":
    unittest.main()
