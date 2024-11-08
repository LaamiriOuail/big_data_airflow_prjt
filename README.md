# Project Setup

## Python Setup
To set up the Python environment, create and activate a virtual environment, then install the required packages:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Airflow Setup
To initialize and start Apache Airflow, make the script executable and run it:
```bash
$ chmod +x ./init.sh
$ ./init.sh
```

```bash
$ chmod +x ./run.sh
$ ./run.sh
```

## PostgreSQL Setup with Docker
To set up PostgreSQL using Docker, follow these steps:
1. Pull the PostgreSQL Docker Image
Pull the latest PostgreSQL Docker image:
```bash
$ docker pull postgres:latest
```

2. Run PostgreSQL Container 
Start a PostgreSQL container with environment variables for database name, user, and password:
```bash
$ docker run -d --name postgres-olap-store -p 5432:5432 \
    -e POSTGRES_DB=olap-store \
    -e POSTGRES_USER=airflow \
    -e POSTGRES_PASSWORD=airflow \
    postgres:latest
```

3. Access PostgreSQL Container
To access the PostgreSQL database, use the following command to start a shell session within the container:
```bash
$ docker exec -it postgres-olap-store psql -U airflow -d olap-store
```

4. Run Initialization Script (`init.sql`)
Initialize the database schema by running the `init.sql` file. If `init.sql` is in your current directory, copy it into the container, and execute it as follows:
```bash
# Copy init.sql into the container
$ docker cp ./data/config/init.sql postgres-olap-store:/init.sql

# Execute init.sql inside the container
$ docker exec -it postgres-olap-store psql -U airflow -d olap-store -f /init.sql
```









