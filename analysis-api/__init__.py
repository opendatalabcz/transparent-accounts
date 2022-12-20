from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from .config import Config

app = Flask(__name__)
app.secret_key = 'dev'
app.config.from_object(Config)

bp = Blueprint('api', __name__)

db = SQLAlchemy(app)

app.register_blueprint(bp, url_prefix='/api')
