from aioredis import create_redis_pool
from functools import wraps

from .config import config


def redis_engine(is_test=False):

    async def _engine(app):
        # Setting up redis pool.
        conf = config['redis']
        app['redis'] = await create_redis_pool(
            (conf['host'], conf['port']),
            minsize=conf['minsize'],
            maxsize=conf['maxsize'],
            db=conf['test_db'] if is_test else conf['db']
        )
        yield

        # Tearing down redis pool.
        app['redis'].close()
        await app['redis'].wait_closed()

    return _engine
