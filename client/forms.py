from wtforms import Form as WTForm, fields as wtf


class Form(WTForm):

	@classmethod
	def redact(cls, *args):
		""" Hide certain fields """
		for arg in args:
			if isinstance(arg, list):
				cls.redact(*arg)
			elif isinstance(arg, str):
				setattr(cls, arg, None)
			else:
				raise TypeError('All redacted field names must be strings.')
		return cls

	@classmethod
	def replace(cls, **kwargs):
		""" Replace certain fields with the specified input field """
		for field, replacements in kwargs.items():
			if isinstance(replacements, str):
				replacements = [replacements]
			if isinstance(replacements, list):
				try:
					[setattr(cls, attr, getattr(wtf, field)()) for attr in replacements]
				except AttributeError:
					raise ValueError('Invalid field name. Must be equivalent of wtf.[key]()')
			else:
				raise ValueError('Replacements must be either strings or lists.')
		return cls