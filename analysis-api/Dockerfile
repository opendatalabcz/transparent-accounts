FROM python:3.10

WORKDIR /analysis-api

COPY requirements.txt ./

# Create virtualenv & install requirements
RUN python3 -m venv venv3 && venv3/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "venv3/bin/flask", "run", "--host=0.0.0.0"]
