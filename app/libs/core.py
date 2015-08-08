from app.libs.base import Entity


class User(Entity):
	"""User object"""

	def __init__(self, **kwargs):
		self.load(**kwargs)