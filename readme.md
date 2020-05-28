## Currency converter HTTP API service

**Disclaimer:** This is not a production service, just a code challenge for the job interview.

### Set up
Install python3 and redis server, then go to project dir and run:
```
pip3 install -r requirements.txt
```

### Run service
```
python3 -m currency_converter.server
```

You can configure service by changing `config.py` or by passing parameter via environment:
```
REDIS_PORT=9999 LOG_LEVEL=ERROR python3 -m currency_converter.server
```

Update rates (all currency rates are stored relative to USD, so USD rate is always `1`):
```
curl -i 'http://127.0.0.1:8088/database?merge=1' \
  -H'Content-Type: application/json; charset=utf-8' \
  -d'{"RUB": 62.15, "EUR": 1.05}'
```

Convert amount from one currency to another:
```
curl -i 'http://127.0.0.1:8088/convert?from=RUB&to=USD&amount=42'
```

### Run tests
```
python3 -m unittest
```
