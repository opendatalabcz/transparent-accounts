import os

from flask import Flask, Blueprint
from sqlalchemy import create_engine
from celery import Celery

app = Flask(__name__)
app.secret_key = 'dev'

bp = Blueprint('api', __name__)

celery = Celery('analysis-api', broker=os.getenv('CELERY_BROKER_URL'))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/postgres'  # TODO
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

from app import controllers

app.register_blueprint(bp, url_prefix='/api')
