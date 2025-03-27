# Glint Solar Case

# Getting starter

The project has a frontend written and a backend.

## Backend

The backend is a Flask application in Python.

#### Installation

Navigate to backend directory and run command below. Might be different for on your system.

```sh
python3.13 -m venv .venv
```

Activate vertial envirionment on MacOS and Linux with `source ./venv/bin/activate`, and `venv/Scripts/activate` for Windows.

Install dependecies:

```sh
pip install -r requirements.txt
```

Run server on localhost:4000:

```sh
py main.py
```

## Frontend

Navigate to the frontend directory and run:

```sh
npm install
```

followed by:

```sh
npm run dev
```

App will be available on localhost:3000

## Task1:

Answer: Max Wave Height: 2.33 for (0.00, 0.00)

```
curl -d '{"lat": 0.00,"lng": 0.00}' -H "Content-Type: application/json"  localhost:4000/location-data
```

## Task2:

Run application

## Task 3:

With a large dataset of historical data I would precalculate the max values so that we limit the amount of compute and processing necessarity during the request. To keep data up to date we could process the daily data and update the precalculated data if any of the values should be overwritten.
Max wave height is likely not the only data the user is interested in, thus, the amount of data could quickly blow up when needing several datasets in order to show the right information. I would strive for doing as little of the data processing on request-time and do as much as possible of the compute before the request.

Caching is also an important factor. Much of historicall data does not change often and is highly cacheable. I would consider implementing caching both on the client and server. On the server we can cache extensively so that we don't have to read and process data from disk, but rather get from memory. On the client we can cache previous requests, in addition to prefetching likely data points the user will request based on for example proximity to current position. This would require debounce to not sendt to many prefetch request to the backend and would also only apply on a certain zoom level.
