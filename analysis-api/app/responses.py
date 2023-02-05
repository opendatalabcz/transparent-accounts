import json

from app import app


def ok_response(json_body: str) -> app.response_class:
    return app.response_class(
        response=json_body,
        content_type='application/json',
        status=200)


def not_found_response(error_message: str) -> app.response_class:
    return app.response_class(
        response=json.dumps({'error': error_message}),
        content_type='application/json',
        status=404)


def bad_request_response(error_message: str) -> app.response_class:
    return app.response_class(
        response=json.dumps({'error': error_message}),
        content_type='application/json',
        status=400)
