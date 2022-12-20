FROM python:3.10

WORKDIR /data-fetcher

COPY ./requirements.txt ./

# create virtualenv & install requirements
# RUN python3 -m venv venv3 && venv3/bin/pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

COPY . .
