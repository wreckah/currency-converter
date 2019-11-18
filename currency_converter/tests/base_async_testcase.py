from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp.web import Application
import logging

from currency_converter.config import config
from currency_converter.redis import redis_engine
from currency_converter.router import route

logging.basicConfig(level=logging.ERROR)


class BaseAsyncTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = Application()
        app.cleanup_ctx.append(redis_engine(True))
        route(app)
        return app

    async def setUpAsync(self):
        await self.app['redis'].select(config['redis']['test_db'])
        await self.app['redis'].flushdb()
