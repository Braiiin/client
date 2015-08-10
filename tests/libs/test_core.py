from client.libs.core import User


class TestUser:
	
	def test_sample_basic(self, app):
		"""Tests sample CRUD"""
		with app.test_request_context('/'):
			# User(
			# 	name='yo',
			#     email='yo@yo.com',
			# 	username='user',
			# 	password='pass'
			# ).post()
			# user = User(name='yo').get()
			# user.email = 'do@do.com'
			# user.put()
			# user.delete()
			pass