


## python :
```bash
$ python3 -m venv venv
$ pip install -r requirements.txt
```


## Airflow :
```bash
$ chmod +x ./init.sh
$ ./init.sh
```

## Couchbase:latest :

```bash
$ docker run -d --name couchbase-server -p 8091-8094:8091-8094 -p 11210:11210 -e COUCHBASE_ADMIN_USERNAME=admin -e COUCHBASE_ADMIN_PASSWORD=admin couchbase
```

