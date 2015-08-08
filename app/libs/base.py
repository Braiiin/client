import requests


class Logic:
	"""Handles communication with logic tier and auth"""
	
	access_token = None
	response = None
	version = 'v1'
	
	def call(self, method, obj, data, func=None):
		"""Assemble URI and make request"""
		if not hasattr(obj, 'id') and not func:
			raise NotImplementedError('As of current, this endpoint is not available.')
		uri = '/api/{v}/{obj}'.format(
			v=self.version, 
			obj=obj.__class__.__name__.lower())
		if hasattr(obj, 'id'):
			uri += '/%s' % obj.id
		if func:
			uri += '/%s' % func
		return self.request(method, uri, data, self.access_token)
	
	def request(self, method, uri, data, access_token=None):
		"""Makes request with specified method, data, and optional access token"""
		if access_token:
			data['access_token'] = access_token
		self.response = getattr(requests, method)(uri, params=data)
		return self.response.json()
	
	def post(self, obj, data):
		"""Post request"""
		return self.request('post', obj, data)
		
	def get(self, obj, data):
		"""Get request"""
		return self.request('get', obj, data)
		
	def put(self, obj, data):
		"""Put request"""
		return self.request('put', obj, data)
		
	def delete(self, obj, data):
		"""Delete request"""
		return self.request('delete', obj, data)


logic = Logic()


class Entity:
	"""Universal entity, abstracts communication with logic tier"""
	
	def load(self, force=False, **kwargs):
		"""Loads all kwargs into object as attributes"""
		for k, v in kwargs.items():
			attr = getattr(self, k)
			if callable(attr) and not force:
				raise AttributeError('Cannot override method, use force=True')
			setattr(self, k, v)
	
	@property
	def _data(self):
		"""Compiles data for this object"""
		return {
			k: v for k, v in vars(self).items()
			if not k.startswith('_') and not callable(v)}
	
	def create(self):
		"""Create object"""
		logic.post(self, self._data)

	def get(self):
		"""Get object"""
		logic.get(self, self._data)

	def save(self):
		"""Saves the object"""
		logic.put(self, self._data)
		
	def delete(self):
		"""Delete the object"""
		logic.delete(self, self._data)
