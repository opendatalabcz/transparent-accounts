FROM python:3.10

WORKDIR /scheduler

# install celery
RUN pip install --no-cache-dir celery

COPY . .

CMD [ "celery", "-A", "app", "beat", "--loglevel=DEBUG"]
