from . import celery, bp


@bp.get('/add')
def add():
    celery.send_task('app.tasks.add', args=[1, 3], kwargs={})
    return "<h1>Success!</h1>"


@bp.get('/test')
def test():
    celery.send_task('app.tasks.test')
    return "<h1>Success!</h1>"


@bp.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
