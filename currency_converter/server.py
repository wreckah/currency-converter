from aiohttp.web import Application, run_app
import logging

from .config import config
from .errors import ServerError, server_error_middleware
from .redis import redis_engine
from .router import route


if __name__ == '__main__':
    logging.basicConfig(level=getattr(logging, config['log_level']))

    app = Application(middlewares=[server_error_middleware])
    app.cleanup_ctx.append(redis_engine())
    route(app)
    run_app(app, host=config['host'], port=config['port'], print=None)
