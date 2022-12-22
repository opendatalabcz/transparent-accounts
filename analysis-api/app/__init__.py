import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

from app.config import Config

app = Flask(__name__)
app.secret_key = 'dev'
app.config.from_object(Config)

bp = Blueprint('api', __name__)

db = SQLAlchemy(app)
celery = Celery('analysis-api', broker=os.getenv('CELERY_BROKER_URL'))

from . import controllers

app.register_blueprint(bp, url_prefix='/api')
