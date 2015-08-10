from client import create_app
import pytest


@pytest.fixture(scope='session')
def app():
	"""New app for test mode"""
	app = create_app(config='TestConfig')
	return app


test = app()