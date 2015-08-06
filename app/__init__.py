"""

App Factory
-----------

uses config.py configurations for setup

"""
import importlib
import logging

from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# login-management
login_manager = LoginManager()
bcrypt = Bcrypt()

logger = logging.getLogger('API')

root = 'app'


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
	
	# initialize encryption mechanism
	bcrypt.init_app(app)
	
	# register all blueprints
	for view in app.config['LIVE']:
		mod = importlib.import_module('%s.%s.views' % (root, view))
		app.register_blueprint(getattr(mod, view))
	
	return app