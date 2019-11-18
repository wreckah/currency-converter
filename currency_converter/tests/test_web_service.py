from aiohttp.test_utils import unittest_run_loop

from .base_async_testcase import BaseAsyncTestCase
from currency_converter.config import config

RUB_RATE = 60.0


def setup_rates(func):
    async def _setup(self):
        await self.app['redis'].mset({'USD': 1.0, 'RUB': RUB_RATE})
        return await func(self)

    return _setup


class CurrencyConvertorTestCase(BaseAsyncTestCase):

    @unittest_run_loop
    @setup_rates
    async def test_convert(self):
        params = {'from': 'RUB', 'to': 'USD', 'amount': 42}
        resp = await self.client.request('GET', '/convert', params=params)
        self.assertEqual(resp.status, 200)

        data = await resp.json()
        self.assertEqual(data['converted_amount'], params['amount'] / RUB_RATE)

    @unittest_run_loop
    @setup_rates
    async def test_unknown_currency(self):
        params = {'from': 'RUB', 'to': 'WRONG', 'amount': 42}
        resp = await self.client.request('GET', '/convert', params=params)
        self.assertEqual(resp.status, 404)

        data = await resp.json()
        self.assertEqual(data['error']['code'], 'not_found')
        self.assertEqual(data['error']['message'], 'Currency WRONG is not found')
        self.assertEqual(data['error']['resource'], 'currency')
        self.assertEqual(data['error']['value'], 'WRONG')

    @unittest_run_loop
    @setup_rates
    async def test_bad_amount(self):
        params = {'from': 'RUB', 'to': 'USD', 'amount': 'lol'}
        resp = await self.client.request('GET', '/convert', params=params)
        self.assertEqual(resp.status, 400)

        data = await resp.json()
        self.assertEqual(data['error']['code'], 'validation_error')
        self.assertEqual(data['error']['fields']['amount'], 'decimal_expected')


class UpdateRatesTestCase(BaseAsyncTestCase):

    @unittest_run_loop
    @setup_rates
    async def test_update(self):
        params = {'RUB': 65}
        resp = await self.client.request('POST', '/database', json=params)
        self.assertEqual(resp.status, 204)

        self.assertEqual(float(await self.app['redis'].get('RUB')), params['RUB'])

    @unittest_run_loop
    @setup_rates
    async def test_update_wo_merge(self):
        data = {'EUR': 0.9}
        resp = await self.client.request('POST', '/database', json=data, params={'merge': 0})
        self.assertEqual(resp.status, 204)

        self.assertEqual(float(await self.app['redis'].get('EUR')), data['EUR'])
        self.assertIsNone(await self.app['redis'].get('RUB'))

    @unittest_run_loop
    @setup_rates
    async def test_bad_rate(self):
        data = {'EUR': 'bad'}
        resp = await self.client.request('POST', '/database', json=data, params={'merge': 0})
        self.assertEqual(resp.status, 400)

        data = await resp.json()
        self.assertEqual(data['error']['code'], 'validation_error')
        self.assertEqual(data['error']['fields']['EUR'], 'decimal_expected')
