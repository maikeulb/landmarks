# Landmarks

Restful API for NYC [Landmarks](http://www1.nyc.gov/site/lpc/index.page)
(unofficial). The resources are the boroughs and their landmarks. Additional
features include hypermedia links, pagination, rate-limiting, and cache
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
| `GET`      | `/api/boroughs`                       | `Retrieve all boroughs`<sub>1</sub>         |
| `GET`      | `/api/boroughs/{bid}`                 | `Retrieve borough`                          |
| `POST`     | `/api/boroughs`                       | `Create borough`                            |
| `PUT`      | `/api/boroughs/{bid}`                 | `Update borough`                            |
| `PATCH`    | `/api/boroughs/{bid}`                 | `Partially update borough`                  |
| `DELETE`   | `/api/boroughs/{bid}`                 | `Delete borough`                            |
| `GET`      | `/api/boroughs/{bid}/landmarks`       | `Retrieve all borough's landmarks`<sub>2</sub>|
| `GET`      | `/api/boroughs/{bid}/landmarks`       | `Retrieve borough's landmark`                 |
| `POST`     | `/api/boroughs/{bid}/landmarks`       | `Create borough landmark`                   |
| `PUT`      | `/api/boroughs/{bid}/landmarks/{id}`  | `Update borough landmark`                   |
| `PATCH`    | `/api/boroughs/{bid}/landmarks/{id}`  | `Partially update borough landmark`         |
| `DELETE`   | `/api/boroughs/{bid}/landmarks/{id}`  | `Delete borough's landmark`                   |

1. Optional query parameters: search_query, order_by
2. Optional query parameters: search_query

Sample Responses
---------------

`http get http://localhost:5000/api/landmarks`
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
        {
            "_links": {
                "self": "/api/boroughs/4"
            }, 
            "id": 4, 
            "name": "Bronx", 
            "number_of_landmarks": 1
        }
    ]
}
```

`http get http://localhost:5000/api/landmarks/1/boroughs`
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
            "name": "1 Wall Street Building"
        }, 
        {
            "_links": {
                "self": "/api/boroughs/1/landmarks/2"
            }, 
            "date_designated": "Tue, 06 Dec 1983 00:00:00 GMT", 
            "description": "Designed in the neo-Gothic style by architect Cass Gilbert. Originally designed to be 420 feet high, the building was eventually elevated to 792 feet.", 
            "id": 2, 
            "name": "Woolworth Building"
        }, 
        {
            "_links": {
                "self": "/api/boroughs/1/landmarks/3"
            }, 
            "date_designated": "Wed, 02 Aug 1967 00:00:00 GMT", 
            "description": "Designed by Thom & Wilson in the Romanesque Revival style.", 
            "id": 3, 
            "name": "Harlem CourtHouse"
        }
    ]
}
```
Run
---
If you have docker installed,
```
docker-compose build
docker-compose up
Go to http://localhost:5000 and visit one of the above endpoints
```

Otherwise, go to `config.py` and point the PostgreSQL and variable
so that they point to your server URI, set the `FLASK_APP` env variable to
landmarks.py, and pip install the requirements. 

After all that has been taken care of,
```
flask db upgrade
flask seed-db
flask run
Go to http://localhost:5000 and visit one of the above endpoints
```
