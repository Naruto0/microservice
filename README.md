# microservice
REST API to create, update and delete a product as defined in the task.

## Easy deploy

Classic __python-flask__ application setup

- create and activate Python `virtualenv` (I prefer _python3_)
- install `pip install -r requirements.txt`

change `ENVVARS` to fit your system (you may take inspiration from `.env_example`)

Create database using _interactive Python shell_ with `SQLAlchemy` method `create_all()`

```
>>> from micro.database import db
>>> db.create_all()
```

Run the application

`$ flask run`

## Middleware

Use _wsgi_ in deployment.