FROM python:3.10

WORKDIR /data-fetcher

COPY ./requirements.txt ./

# create virtualenv & install requirements
RUN python3 -m venv venv3 && venv3/bin/pip install --no-cache-dir -r requirements.txt

# TEMPORARY while SQLAlchemy 2.0 is still in beta
RUN yes | venv3/bin/pip uninstall sqlalchemy && venv3/bin/pip install sqlalchemy==2.0.0b4

COPY . .

ENTRYPOINT ["/data-fetcher/dockerize/entrypoint.sh"]
