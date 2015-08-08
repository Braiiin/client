"""

Configurations
--------------

Various setups for different app instances

"""


class Config:
	"""Default config"""
	
	DEBUG = False
	TESTING = False
	SECRET_KEY = 'flask+mongoengine=<3'
	SESSION_STORE = 'session'
	LIVE = ['public', 'sphere']
	STATIC_PATH = 'static'
	
	INIT = {
		'port': 8000,
		'host': '127.0.0.1',
	}
	
	
class ProductionConfig(Config):
	"""Production vars"""
	pass


class DevelopmentConfig(Config):
	"""For local runs"""
	DEBUG = True
	
	
class TestConfig(Config):
	"""For automated testing"""
	TESTING = True