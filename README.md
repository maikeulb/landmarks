# Landmarks

Restful API for NYC [Landmarks](http://www1.nyc.gov/site/lpc/index.page) (unofficial). The resources are the boroughs and their
landmarks. Additional features include pagination, rate-limiting, and cache headers.

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

Sample Response
---------------
[TODO]

Run
---
If you have docker installed,
```
docker-compose build
docker-compose up
Go to http://localhost:5000 and visit one of the above endpoints
```

Otherwise, go to config.py and point the PostgreSQL and Elasticsearch variables
so that they point to your server URI's, set the FLASK_APP env variable to
landmarks.py, and pip install the requirements. 

After all that has been taken care of,
```
flask db upgrade
flask seed-db
flask run
Go to http://localhost:5000 and visit one of the above endpoints
```
