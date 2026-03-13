import flask
import functions_framework

@functions_framework.http
def hello_http(request: flask.Request) -> flask.typing.ResponseReturnValue:
    return "Hello world!"