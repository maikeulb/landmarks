# Landmarks

Restful API for NYC [Landmarks](http://www1.nyc.gov/site/lpc/index.page)
(unofficial). The resources are the boroughs and their landmarks. Additional
features include hypermedia links, pagination, search/order, rate-limiting, and cache
headers. This application is written using flask with minimal dependencies (not
using a rest framework).

Technology
----------
* Flask
* PostgreSQL

Endpoints
---------

| Method     | URI                                   | Action                                      |
|------------|---------------------------------------|---------------------------------------------|
| `GET`      | `/api/boroughs`                       | `Retrieve all boroughs`<sup>1</sup>         |
| `GET`      | `/api/boroughs/{bid}`                 | `Retrieve borough`                          |
| `POST`     | `/api/boroughs`                       | `Create borough`                            |
| `PUT`      | `/api/boroughs/{bid}`                 | `Update borough`                            |
| `PATCH`    | `/api/boroughs/{bid}`                 | `Partially update borough`<sup>2</sup>                  |
| `DELETE`   | `/api/boroughs/{bid}`                 | `Delete borough`                            |
| `GET`      | `/api/boroughs/{bid}/landmarks`       | `Retrieve all borough landmarks`<sup>3</sup>|
| `GET`      | `/api/boroughs/{bid}/landmarks/{id}`  | `Retrieve borough landmark`                 |
| `POST`     | `/api/boroughs/{bid}/landmarks`       | `Create borough landmark`                   |
| `PUT`      | `/api/boroughs/{bid}/landmarks/{id}`  | `Update borough landmark`                   |
| `PATCH`    | `/api/boroughs/{bid}/landmarks/{id}`  | `Partially update borough landmark`<sup>2</sup> |
| `DELETE`   | `/api/boroughs/{bid}/landmarks/{id}`  | `Delete borough's landmark`                 |

1. Optional query parameters: search_query, order_by
2. Send only the fields you need to update
3. Optional query parameters: search_query

Sample Responses
---------------

`http get http://localhost:5000/api/boroughs`
```
{
    "_links": {
        "next": null, 
        "prev": null, 
        "self": "/api/boroughs?page=1&per_page=10"
    }, 
    "_meta": {
        "page": 1, 
        "per_page": 10, 
        "total_items": 4, 
        "total_pages": 1
    }, 
    "items": [
        {
            "_links": {
                "self": "/api/boroughs/1"
            }, 
            "id": 1, 
            "name": "Manhattan", 
            "number_of_landmarks": 3
        }, 
        {
            "_links": {
                "self": "/api/boroughs/2"
            }, 
            "id": 2, 
            "name": "Brooklyn", 
            "number_of_landmarks": 1
        }, 
        {
            "_links": {
                "self": "/api/boroughs/3"
            }, 
            "id": 3, 
            "name": "Queens", 
            "number_of_landmarks": 2
        }, 
...
```

`http get http://localhost:5000/api/boroughs/1/landmarks`
```
{
    "_links": {
        "next": null, 
        "prev": null, 
        "self": "/api/boroughs/1/landmarks?page=1&per_page=10"
    }, 
    "_meta": {
        "page": 1, 
        "per_page": 10, 
        "total_items": 3, 
        "total_pages": 1
    }, 
    "items": [
        {
            "_links": {
                "self": "/api/boroughs/1/landmarks/1"
            }, 
            "date_designated": "Tue, 06 Mar 2001 00:00:00 GMT", 
            "description": "Art-Deco-style skyscraper designed by Ralph Walker,originally built for the Irving Trust Company.", 
            "id": 1, 
            "borough_id": 1, 
            "name": "1 Wall Street Building"
        }, 
...
```
Run
---
If you have docker installed,
```
docker-compose build
docker-compose up
Go to http://localhost:5000 and visit one of the above endpoints
```

Alternatively, create a database named 'landmarks', open `config.py` and point
the database URI to your server, set the `FLASK_APP` env variable to
landmarks.py, and install the dependencies (e.g. `pip install -r
requirements.txt`)

`cd` into `./src` (if you are not already) and run the following:
```
flask db upgrade
flask seed-db
flask run
Go to http://localhost:5000 and visit one of the above endpoints
```
