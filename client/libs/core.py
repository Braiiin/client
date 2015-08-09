from client.libs.base import Entity


class User(Entity):
	"""User object"""
	
	access_token = None

	def is_active(self):
		"""If the user is considered 'active' in application"""
		return getattr(self, 'status', 'inactive') == 'active'

	def is_authenticated(self):
		"""Method of checking authentication"""
		return self.access_token is not None

	def is_anonymous(self):
		"""If the user is not logged in"""
		return self.access_token is None

	def get_id(self):
		"""ID for the current user object"""
		return self.access_token
	
	def authenticate(self, **kwargs):
		"""authenticate by creating session and loading user object"""
		return self.load(**kwargs).get()
	
	
class Session(Entity):
	"""Session object"""