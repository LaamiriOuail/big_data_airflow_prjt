#!/bin/bash

# Initialize the Airflow database
echo "Initializing the Airflow database..."
airflow db init

# Start the Airflow web server on port 8080 in the background
echo "Starting the Airflow web server on port 8080..."
airflow webserver --port 8080 &

# Start the Airflow scheduler in the background
echo "Starting the Airflow scheduler..."
airflow scheduler &

# Wait for both background processes to finish
wait
