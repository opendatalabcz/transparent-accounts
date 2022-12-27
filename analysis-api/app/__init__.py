import os

from flask import Flask, Blueprint
from sqlalchemy import create_engine
from celery import Celery

import app.models
from app.config import Config

app = Flask(__name__)
app.secret_key = 'dev'
app.config.from_object(Config)

bp = Blueprint('api', __name__)

celery = Celery('analysis-api', broker=os.getenv('CELERY_BROKER_URL'))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/postgres'
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

from . import controllers

app.register_blueprint(bp, url_prefix='/api')
