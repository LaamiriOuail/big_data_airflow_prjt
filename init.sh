#!/bin/bash


export AIRFLOW_HOME=/home/hajar/big_data_airflow_prjt/airflow
# Initialize the Airflow database
echo "Initializing the Airflow database..."
airflow db migrate

airflow users create \
    --username admin \
    --firstname ouail \
    --lastname laamiri \
    --role Admin \
    --email laamiriouail@gmail.com

# Start the Airflow web server on port 8080 in the background
echo "Starting the Airflow web server on port 8080..."
airflow webserver --port 8080 &

# Start the Airflow scheduler in the background
echo "Starting the Airflow scheduler..."
airflow scheduler &

# Wait for both background processes to finish
wait
