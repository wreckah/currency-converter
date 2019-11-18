from aiohttp.web import HTTPClientError, middleware
from json import dumps
from typing import Dict
from traceback import format_exception
import logging

from .config import config

logger = logging.getLogger('currency_converter.server')


class ServerError(HTTPClientError):
    status_code = 500

    def __init__(self) -> None:
        error_body = {
            'error': {
                  'code': 'server_error',
                  'message': 'Unexpected server error',
            },
        }
        super().__init__(text=dumps(error_body), content_type='application/json')


class ValidationError(HTTPClientError):
    status_code = 400

    def __init__(self, fields: Dict, **extra) -> None:
        error_body = {
            'error': {
                  'code': 'validation_error',
                  'message': 'Validation error',
                  'fields': fields,
            },
        }
        error_body['error'].update(**extra)
        super().__init__(text=dumps(error_body), content_type='application/json')


class NotFoundError(HTTPClientError):
    status_code = 404

    def __init__(self, resource, value) -> None:
        error_body = {
            'error': {
                'code': 'not_found',
                'message': '{} {} is not found'.format(resource.capitalize(), value),
                'resource': resource,
                'value': value,
            }
        }
        super().__init__(text=dumps(error_body), content_type='application/json')


@middleware
async def server_error_middleware(request, handler):
    try:
        response = await handler(request)
    except HTTPClientError:
        raise
    except Exception as error:
        logger.error(''.join(format_exception(None, error, error.__traceback__)))
        return ServerError()
    else:
        return response
