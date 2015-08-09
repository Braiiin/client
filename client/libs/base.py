import datetime
from client.exceptions import LogicException, ClientException
from flask import current_app
from client import logger
import requests


class Logic:
	"""Handles communication with logic tier and auth"""
	
	access_token = None
	response = None
	version = 'v1'
	
	def call(self, method, obj, data, func=None):
		"""Assemble URI and make request"""
		uri = '{logic}/api/{v}/{obj}'.format(
			logic=current_app.config['LOGIC_URI'],
			v=self.version, 
			obj=obj.__class__.__name__.lower())
		if hasattr(obj, 'id'):
			uri += '/%s' % obj.id
		if func:
			uri += '/%s' % func
		return self.request(method, uri, data, self.access_token)
	
	def request(self, method, uri, data, access_token=None):
		"""Makes request with specified method, data, and optional access token"""
		data = data or {}
		if access_token:
			data['access_token'] = access_token
		self.response = getattr(requests, method)(uri, params=data)
		json = self.response.json()
		logger.info(self.response.url)
		logger.debug(json)
		if json['status'] != 200:
			raise LogicException('%s\n- - "%s %s" %d -' % (
				json['message'], method.upper(), self.response.url, json['status']))
		return json['data']
	
	# TODO: do we need these? call() is invoked directly
	def post(self, obj, **data):
		"""Post request"""
		return self.call('post', obj, data)
		
	def get(self, obj, **data):
		"""Get request"""
		return self.call('get', obj, data)
		
	def put(self, obj, **data):
		"""Put request"""
		return self.call('put', obj, data)
		
	def delete(self, obj, **data):
		"""Delete request"""
		return self.call('delete', obj, data)


logic = Logic()


class Entity:
	"""Universal entity, abstracts communication with logic tier"""

	def __init__(self, **kwargs):
		self.load(**kwargs)
	
	def load(self, force=False, **kwargs):
		"""Loads all kwargs into object as attributes"""
		for k, v in kwargs.items():
			attr = getattr(self, k, None)
			if callable(attr) and not force:
				raise ClientException(
					'Cannot override method "%s", use force=True' % k)
			setattr(self, k, v)
		return self
	
	@property
	def _data(self):
		"""Compiles data for this object"""
		return {
			k: v for k, v in vars(self).items()
			if not k.startswith('_') and not callable(v)}
	
	def call(self, method, data=None, **kwargs):
		"""calls the logic tier"""
		response = logic.call(method, self, data or self._data, **kwargs)
		to_date = datetime.datetime.fromtimestamp
		_values = {
			'_id': lambda v: v['$oid'],
			'created_at': lambda v: v['$date'],  #TODO: fix to_date
		    'updated_at': lambda v: v['$date'],
		}
		_keys, identity = {'_id': 'id'}, lambda x: x
		data = {_keys.get(k, k): _values.get(k, identity)(v) for k, v
		        in response.items()}
		logger.info(data)
		return self.load(**data)

	def create(self):
		"""Create object"""
		return self.call('post')

	def get(self):
		"""Get object"""
		return self.call('get')

	def save(self):
		"""Saves the object"""
		return self.call('put')
		
	def delete(self):
		"""Delete the object"""
		return self.call('delete')
