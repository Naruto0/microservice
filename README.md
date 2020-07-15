# microservice
REST API to create, update and delete a product as defined in the task.

## Easy develop/deploy

#### setup the database

Classic __python-flask__ application setup

#### install requirements

- create and activate Python `virtualenv` (I prefer _python3_)
- install `pip install -r requirements.txt`

#### setup environment variables

change `ENVVARS` to fit your system (you may take inspiration from `.env_example`)
```
export FLASK_APP=micro  # for developement
export DATABASE=postgres://clerk:spersecret@localhost:5432/catalog
```

Or you can use `dotenv` module and load `.env` from base folder.

Create database using _interactive Python shell_ with `SQLAlchemy` method `create_all()`

```
>>> from micro.database import db
>>> db.create_all()
```

Run the application

`$ flask run`

## Middleware

Use _wsgi_ in deployment. There is used `wsgi.ini` with heroku on mockup server.

```
$ flask db init
$ flask db migrate
```
