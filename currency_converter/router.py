from .api import convert, store


def route(app):
    app.router.add_route('GET', '/convert', convert)
    app.router.add_route('POST', '/database', store)
