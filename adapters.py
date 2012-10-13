

class Adapter:
	avaliable_adapters = {
		'sqlite':'sqlite3',
		'postgresql':'pycopg2',
		'mysql':'MySQLdb'
		}
	operations = {
		'lt' : '<',
		'lte' : '<=',
		'gt' : '>',
		'gte' : '>=',
		'eq' : '=',
		'ne' : '!=',
		'in' : 'IN',
		'is' : 'IS',
		'isnull' : 'IS NULL',
		'between' : 'BETWEEN {0} AND {1}',
	}

	def import_a(self, db):
		if db in self.avaliable_adapters:
			try:
				return __import__(self.avaliable_adapters[db])
			except:
				raise ImproperlyConfigured('Adapter Not supported.')
		raise NotImplementedError('Adapter not avaliable, specify on of {adpters}'.format(adapters=self.avaliable_adapters.keys()))

	def connect(self, *args, **kwargs):
		raise NotImplementedError('Implement in subclass.')

class SqliteAdapter(Adapter):
	def __init__(self, database, **kwargs):
		self.sqlite = self.import_a('sqlite')
		self.operations = {
			'ieq' : 'LIKE %(v)s ESCAPE',
			'icontains' : 'GLOB %(v)s',
			'istartswith' : 'LIKE %(v)s ESCAPE',
			'startwith' : 'GLOB %(v)s'
			}.update(Adapter.operations)
	
	def connect(self, database, **kwargs):
		return self.sqlite.connect(database, **kwargs)
