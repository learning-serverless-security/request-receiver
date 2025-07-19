from flask import Flask, request
from datetime import datetime, UTC
from contextlib import contextmanager


def print_pair(*args):
    if len(args) == 2:
        key, value = args
        label = f"{key}:"
        print(f"{label:<25}{value}")
    else:
        print(args[0])


@contextmanager
def info(label):
    print_line()
    print(label)
    print_line()
    yield print_pair
    print_line()


def print_line():
    print("-" * 100)


METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
app = Flask(__name__)

@app.route('/', methods=METHODS)
@app.route('/<path:path>', methods=METHODS)
def catch_all(path=''):
    with info("NEW REQUEST") as p:
        p("Time", datetime.now(UTC))
        p("Method", request.method)
        p("Path", request.path)

    with info("HEADERS") as p:
        for key, value in dict(request.headers).items():
            p(f"{key}", value)

    with info("BODY") as p:
        p(request.get_data(as_text=True))

    return 'Request received\n', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
