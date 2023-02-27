import logging
import os

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

# TODO: move to config
banks = [
    {
        'shortcut': Bank.CSAS.name,
        'name': 'Česká spořitelna',
        'url': 'https://www.csas.cz/',
        'code': Bank.CSAS.value,
        'accounts_count': None
    },
    {
        'shortcut': Bank.CSOB.name,
        'name': 'Československá obchodní banka',
        'url': 'https://www.csob.cz/',
        'code': Bank.CSOB.value,
        'accounts_count': None
    },
    {
        'shortcut': Bank.FIO.name,
        'name': 'Fio banka',
        'url': 'https://www.fio.cz/',
        'code': Bank.FIO.value,
        'accounts_count': None
    },
    {
        'shortcut': Bank.KB.name,
        'name': 'Komerční banka',
        'url': 'https://www.kb.cz/',
        'code': Bank.KB.value,
        'accounts_count': None
    },
    {
        'shortcut': Bank.MONETA.name,
        'name': 'Moneta Money Bank',
        'url': 'https://www.moneta.cz/',
        'code': Bank.MONETA.value,
        'accounts_count': None
    },
    {
        'shortcut': Bank.RB.name,
        'name': 'Raiffeisenbank',
        'url': 'https://www.rb.cz/',
        'code': Bank.RB.value,
        'accounts_count': None
    }
]

from app import controllers

app.register_blueprint(bp, url_prefix='/api')
