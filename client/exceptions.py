from client import logger

class ClientException(Exception):
	"""general exception for all client errors"""
	message = None

	def __init__(self, message=None):
		super().__init__(message)
		logger.exception(message)
		self.message = message or self.message


class LogicException(Exception):
	"""default error for API errors"""
	message = 'There was an error processing your request'