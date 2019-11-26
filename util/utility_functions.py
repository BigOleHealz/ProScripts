from datetime import datetime

def timer(func) -> list:
	"""
	Timer function for use as a decorator
	param type func: Description of parameter `func`.
	:return: Description of returned object.
	"""
	def wrapper(*args, **kwargs):
		start_time = datetime.now()
		funcy = func(*args, **kwargs)
		diff = datetime.now() - start_time
		print(diff)
		return [funcy, diff]
	return wrapper