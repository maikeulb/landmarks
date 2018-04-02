# Landmarks

Restful API for NYC [Landmarks(LPC)](http://www1.nyc.gov/site/lpc/index.page). The resources are the boroughs and their
Landmarks. 

Technology
----------
* Flask
* PostgreSQL

## Endpoints

| Method     | URI                                   |
|------------|---------------------------------------|
| `GET`      | `/api/boroughs`                       |
| `GET`      | `/api/boroughs/{bid}`                 |
| `POST`     | `/api/boroughs`                       |
| `PUT`      | `/api/boroughs/{bid}`                 |
| `PATCH`    | `/api/boroughs/{bid}`                 |
| `DELETE`   | `/api/boroughs/{bid}/landmarks`       |
| `GET`      | `/api/boroughs/{bid}/landmarks`       |
| `GET`      | `/api/boroughs/{bid}/landmarks`       |
| `PUT`      | `/api/boroughs/{bid}/landmarks/{id}`  |
| `PATCH`    | `/api/boroughs/{bid}/landmarks/{id}`  |
| `DELETE`   | `/api/boroughs/{bid}/landmarks/{id}`  |


Run
---
If you have docker installed,
```
docker-compose build
docker-compose up
Go to http://localhost:5000 and visit one of the above endpoints
```

Otherwise, go to config.py and point the Postgresql and Elasticsearh variables so
that they point to your server URI's, set the FLASK_APP env variable to
elasticblog, and pip install the requirements. 

After all that has been taken care of,
```
flask db upgrade
flask seed-db
flask run
Go to http://localhost:5000 and visit one of the above endpoints
```
```
