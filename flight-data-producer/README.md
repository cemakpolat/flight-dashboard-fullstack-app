
# Flight Data Producer

This project simulates a flight data producer that publishes data to an MQTT broker. It generates random flight information (flight ID, altitude, fuel level, status, etc.) and sends it to a specified MQTT topic at a configurable interval.

## Prerequisites

*   Python 3.6 or higher
*   Docker (recommended)
*   Docker Compose (recommended)

## Installation (Local Python Environment - Not Recommended)

**Note:** Using Docker is the recommended way to run this project. The instructions below are provided for local execution but may require more manual setup and dependency management.

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd <your_project_directory>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**

    You can set environment variables directly in your shell (e.g., using `export` on Linux/macOS or `$env:` on PowerShell) or create a `.env` file in the project directory:

    ```
    MQTT_BROKER=broker.emqx.io
    MQTT_PORT=1883
    MQTT_TOPIC=flights/topic
    MESSAGE_SENDING_INTERVAL=10
    CITIES=NewYork,London,Paris
    ```

5.  **Run the script:**

    ```bash
    python your_script_name.py  # Replace with the actual script name
    ```

## Installation and Execution (Using Docker Compose - Recommended)

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd <your_project_directory>
    ```

2.  **Create a `requirements.txt` file:**  This file should list all the Python dependencies required by your script (e.g., `paho-mqtt`). If you don't have any, you'll still need to create an empty `requirements.txt`

3.  **Create a `Dockerfile`:**  Create a file named `Dockerfile` in the same directory as the `docker-compose.yml` file.  Use the following content:

    ```dockerfile
    FROM python:3.9-slim-buster

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    CMD ["python", "your_script_name.py"] # Replace with your script's name
    ```
    **Important:** Replace `your_script_name.py` in the `Dockerfile` with the *actual* name of your Python script.

4.  **Configure environment variables in `docker-compose.yml`:** Edit the `docker-compose.yml` file to set the desired values for `MQTT_BROKER`, `MQTT_PORT`, `MQTT_TOPIC`, `MESSAGE_SENDING_INTERVAL`, and `CITIES`.

    ```yaml
    version: "3.9"
    services:
      flight-data-producer:
        build:
          context: .
          dockerfile: Dockerfile
        volumes:
          - .:/app
        environment:
          - PYTHONUNBUFFERED=1
          - MQTT_BROKER=broker.emqx.io
          - MQTT_PORT=1883
          - MQTT_TOPIC=flights/topic
          - MESSAGE_SENDING_INTERVAL=10
          - CITIES=NewYork,London,Paris,Tokyo,Sydney,Dubai,Berlin,Rome,Madrid,Toronto,LosAngeles,Chicago,Houston,Phoenix,Philadelphia,SanAntonio,SanDiego,Dallas,SanJose,Austin
        depends_on:
          []
        restart: always

      mqtt-broker:
        image: eclipse-mosquitto:latest
        ports:
          - "1883:1883"
    ```

5.  **Build and run the application:**

    ```bash
    docker-compose up --build
    ```

6.  **Stop the application:**

    ```bash
    docker-compose down
    ```

## Configuration

The following environment variables can be used to configure the application:

*   `MQTT_BROKER`: The address of the MQTT broker.  Defaults to `broker.emqx.io`.
*   `MQTT_PORT`: The port of the MQTT broker. Defaults to `1883`.
*   `MQTT_TOPIC`: The MQTT topic to publish data to. Defaults to `flights/topic`.
*   `MESSAGE_SENDING_INTERVAL`: The interval (in seconds) between sending messages. Defaults to `10`.
*   `CITIES`: A comma-separated list of cities used for generating flight data. Defaults to a list of major cities.

## Troubleshooting

*   **Connection errors:** Verify that the MQTT broker is running and accessible from your machine or Docker container. Check the `MQTT_BROKER` and `MQTT_PORT` configuration.
*   **Missing dependencies:** If running locally, ensure that all required Python packages are installed using `pip install -r requirements.txt`. If running with Docker, check the `Dockerfile` and ensure that all dependencies are installed correctly.
*   **Docker build errors:** Check the `Dockerfile` for any syntax errors or missing files. Make sure the `context` in the `docker-compose.yml` file is set correctly.
*   **No data published:** Verify the MQTT topic and ensure that a subscriber is listening to the topic. Check the application logs for any errors.

## License

 MIT License



