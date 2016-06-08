import json
from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, tuple):
			data = {}
			for obj in o:
				data.update(self.parse_sqlalchemy_object(obj))
			return data
		if isinstance(o.__class__, DeclarativeMeta):
			return self.parse_sqlalchemy_object(o)
		return json.JSONEncoder.default(self, o)

	def parse_sqlalchemy_object(self, o, cls=[]):
		cls.append(o.__class__)
		data = {}
		fields = o.__json__() if hasattr(o, '__json__') else dir(o)
		for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
			value = o.__getattribute__(field)
			if isinstance(value, list):
				for v in value:
					if v.__class__ not in cls:
						#value = list()
						value = self.parse_sqlalchemy_object(v)
			try:
				json.dumps(value)
				data[field] = value
			except TypeError:
				data[field] = None
		cls.pop()
		return data