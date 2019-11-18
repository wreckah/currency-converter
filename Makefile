lint:
	@pylint -E currency_converter

test:
	@cd ./currency_converter
	@python3 -m unittest

run:
	@cd ./currency_converter
	@python3 -m currency_converter.server
