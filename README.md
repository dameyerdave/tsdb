# Time Series Database

This is a prove of concept on how to integrate Timeseries database into Django and display the data using apex charts.

## Quick start

1. Clone the repository

```
git clone https://github.com/dameyerdave/tsdb
```

2. Change into the directory and start the docker containers

```bash
cd tsdb
make run
```

3. Insert some testing data

```bash
sudo powermetrics -s smc | docker exec -i tsdb-api-1 ./manage.py macmetrics
```

4. Open the browser to see the data

[http://localhost:8091](http://localhost:8091)
