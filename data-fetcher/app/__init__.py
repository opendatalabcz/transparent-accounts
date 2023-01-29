import logging

from sqlalchemy import create_engine

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')
# SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/postgres'


engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
