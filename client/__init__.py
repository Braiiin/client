"""

App Factory
-----------

uses config.py configurations for setup

"""
import importlib
import logging

from flask import Flask
from flask_hashing import Hashing
from flask_login import LoginManager

# login-management
login_manager = LoginManager()
hashing = Hashing()

logger = logging.getLogger('Client')
logging.basicConfig(level=logging.DEBUG)

root = 'client'


def create_app(config='DevelopmentConfig', **configs):
	"""
	App factory
	:param config: name of Config class from config.py
	"""

	# Create and set app config
	app = Flask(__name__)
	app.config.from_object('%s.config.%s' % (root, config))
	app.config.update(**configs)

	# initialize Flask-Login with app
	login_manager.init_app(app)
	
	# initialize hash mechanism
	hashing.init_app(app)

	# Setup blueprints
	def register_blueprints():
		for view in app.config['LIVE']:
			mod = importlib.import_module('%s.%s.views' % (root, view))
			app.register_blueprint(getattr(mod, view))

	app.register_blueprints = register_blueprints
	app.register_blueprints()
	
	return app