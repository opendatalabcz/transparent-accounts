FROM python:3.10

WORKDIR /data-fetcher

COPY ./requirements.txt ./

# Create virtualenv & install requirements
RUN python3 -m venv venv3 && venv3/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

# Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.10.0/wait /wait
RUN chmod +x /wait

ENTRYPOINT ["/data-fetcher/dockerize/entrypoint.sh"]
