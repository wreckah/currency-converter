from aiohttp.web import json_response, Request, Response
from currency_converter.errors import NotFoundError, ValidationError


async def convert(request: Request) -> Response:
    """
    GET /convert?from=RUB&to=USD&amount=42
    """
    amount = request.query.get('amount')
    if not amount:
        raise ValidationError({'amount': 'required'})
    try:
        amount = float(amount)
    except ValueError:
        raise ValidationError({'amount': 'decimal_expected'})

    from_cur = request.query.get('from')
    if not from_cur:
        raise ValidationError({'from': 'required'})
    to_cur = request.query.get('to')
    if not to_cur:
        raise ValidationError({'to': 'required'})

    from_rate, to_rate = await request.app['redis'].mget(from_cur, to_cur)
    if not from_rate:
        raise NotFoundError('currency', from_cur)
    if not to_rate:
        raise NotFoundError('currency', to_cur)

    return json_response({
        'converted_amount': amount / float(from_rate) * float(to_rate)
    })


async def store(request: Request) -> Response:
    """
    POST /database?merge=1
    Content-Type: application/json

    {"RUB": 62.15, "USD": 1}
    """
    merge = request.query.get('merge')
    if merge == '0':
        await request.app['redis'].flushdb()

    rates = await request.json()
    data = {}
    for key in rates:
        try:
            data[key] = float(rates[key])
        except ValueError:
            raise ValidationError({key: 'decimal_expected'})
    data['USD'] = 1
    await request.app['redis'].mset(rates)

    return Response(status=204)
