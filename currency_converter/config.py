from os import environ

config = {
    'host': environ.get('HOST', '127.0.0.1'),
    'port': int(environ.get('PORT', 8088)),
    'log_level': environ.get('LOG_LEVEL', 'DEBUG'),
    'redis': {
        'host': environ.get('REDIS_HOST', '127.0.0.1'),
        'port': int(environ.get('REDIS_PORT', 6379)),
        'minsize': int(environ.get('REDIS_MINSIZE', 1)),
        'maxsize': int(environ.get('REDIS_MINSIZE', 5)),
        'db': int(environ.get('REDIS_DB', 7)),
        'test_db': int(environ.get('REDIS_TEST_DB', 8)),
    },
}
