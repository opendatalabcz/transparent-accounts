FROM python:3.10

WORKDIR /analysis-api

COPY requirements.txt ./

# create virtualenv & install requirements
RUN python3 -m venv venv3 && venv3/bin/pip install --no-cache-dir -r requirements.txt

# TEMPORARY while SQLAlchemy 2.0 is still in beta
RUN yes | venv3/bin/pip uninstall sqlalchemy && venv3/bin/pip install sqlalchemy==2.0.0b4

COPY . .
CMD [ "venv3/bin/flask", "--debug", "run", "--host=0.0.0.0"]
