import logging
import os
import json

from celery import Celery
from flask import Flask, Blueprint
from flask_cors import CORS
from sqlalchemy import create_engine

from app.models import Bank

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
CORS(app)  # Enable cross-origin resource sharing

bp = Blueprint('api', __name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

# Connection to Celery
celery = Celery('analysis-api', broker=os.getenv('CELERY_BROKER_URL'))

# Connection to database
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DB_URI)

# Load banks details from JSON file
with open('banks.json') as json_file:
    banks = json.load(json_file)

# Register API
from app.apis import blueprint as api

app.register_blueprint(api, url_prefix='/api')
