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


def create_app(_name_=None, config='DevelopmentConfig', **configs):
	"""
	App factory
	:param config: name of Config class from config.py
	"""

	# Create and set app config
	app = Flask(_name_ or __name__)
	app.config.from_object('%s.config.%s' % (root, config))
	app.config.update(**configs)

	# initialize Flask-Login with app
	login_manager.init_app(app)
	
	# initialize hash mechanism
	hashing.init_app(app)
	
	# setup blueprints
	def reload_blueprints():
		"""Loads all LIVE blueprints"""
		mod = lambda view: importlib.import_module('%s.%s.views' % (root, view))
		return [getattr(mod(view), view) for view in app.config['LIVE']]

	# Setup blueprints
	def register_blueprints(*blueprints):
		"""Registers all passed-in blueprints"""
		blueprints = list(blueprints) + reload_blueprints()
		for blueprint in blueprints:
			app.register_blueprint(blueprint)

	app.register_blueprints = register_blueprints
	app.register_blueprints()
	
	return app