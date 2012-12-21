

class NotImplementedError(Exception):
	def __str__(self):
		return "This operation is not implemented."


class ImproperlyConfigured(Exception):
	pass
