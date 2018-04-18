from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

from api.endpoint import endpoint_api

from gather import tasks
from gather import celery

from database import db
from database import cache

import sys

# Setup flask
app = Flask(__name__)
app.config.from_object('config.Config')

# Set up API
api_instance = Api(doc='/api/',
                   version='v1.0',
                   title='falcon.io Case API',
                   description='This is the API for the falcon.io case.')

api_instance.add_namespace(endpoint_api, path='/endpoint')
api_instance.init_app(app) # Initialize the api

TaskBase = celery.Task # Fiddle with celery because Flask needs to be able to work with celery, and without this bit celery doesn't have the correct app context.
class ContextTask(TaskBase):
    abstract = True
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)
celery.Task = ContextTask

# Set up database
db.init_app(app) # Initialize the database with the app
print("Resetting the database")
db.drop_all(app=app) # Drop the table here, so we have a fresh start every time.
db.create_all(app=app) # If the database table doesn't already exist, then create it here. 

# Setup cache
cache.init_app(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=80)