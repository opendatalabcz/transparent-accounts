import logging
import os

from celery import Celery
from flask import Flask, Blueprint
from flask_cors import CORS
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = 'dev'
CORS(app)

bp = Blueprint('api', __name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

celery = Celery('analysis-api', broker=os.getenv('CELERY_BROKER_URL'))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/postgres'  # TODO
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

from app import controllers

app.register_blueprint(bp, url_prefix='/api')
