import logging
import os
import json

from celery import Celery
from flask import Flask, Blueprint
from flask_cors import CORS
from sqlalchemy import create_engine

from app.models import Bank

app = Flask(__name__)
app.secret_key = 'dev'
CORS(app)  # TODO remove in production

bp = Blueprint('api', __name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

celery = Celery('analysis-api', broker=os.getenv('CELERY_BROKER_URL'))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/postgres'  # TODO move to config
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# Load banks details from JSON file
with open('banks.json') as json_file:
    banks = json.load(json_file)

from app.apis import blueprint as api

app.register_blueprint(api, url_prefix='/api')
