"""

Configurations
--------------

Various setups for different app instances

"""


class Config:
	"""Default config"""
	
	DEBUG = False
	TESTING = False
	SECRET_KEY = 'flask+braiiin=<3'
	SESSION_STORE = 'session'
	LIVE = ['public', 'sphere']
	STATIC_PATH = 'static'
	HASHING_ROUNDS = 15
	
	INIT = {
		'port': 8000,
		'host': '127.0.0.1',
	}
	
	
class ProductionConfig(Config):
	"""Production vars"""
	LOGIC_URI = ''


class DevelopmentConfig(Config):
	"""For local runs"""
	DEBUG = True
	LOGIC_URI = 'http://localhost:8001'
	
	
class TestConfig(Config):
	"""For automated testing"""
	TESTING = True