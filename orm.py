from .exceptions import ImproperlyConfigured


class Database:
	def __init__(self, adapter = None):
		assert adapter, "Empty adapter !!!"
		self.adapter = adapter

	def connect(self):
		return self.adapter.connect()
	
	def execute(self, query):
		pass

class Adapter:
	avaliable_adapters = {
		'sqlite':'sqlite3',
		'postgresql':'pycopg2',
		'mysql':'MySQLdb'
		}
	operations = {
		'lt' : '{field} < {val}',
		'lte' : '{field} <= {val}',
		'gt' : '{field} > {val}',
		'gte' : '{field} >= {val}',
		'eq' : '{field} = {val}',
		'ne' : '{field} != {val}',
		'in' : '{field} IN {val}',
		'is' : '{field} IS {val}',
		'isnull' : '{field} IS NULL {val}',
		'between' : '{field} BETWEEN {val} AND {val_1}',
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


class Query(object):
	select_frame = "SELECT * FROM {table} WHERE {clause};"
	select_all_frame = "SELECT * FROM {table};"

	def __init__(self, database):
		#TO-DO pick right adapter according to database.
		self.adapter = SqliteAdapter(database)

	def _prepare_where_string(self, **kwargs):
		query = ''
		for fo, v in kwargs.items():
			field, operation = fo.split('__')
			if operation in SqliteAdapter.operations:
				if operation == 'in':
					val = ', '.join([str(x) for x in v])
					val = '('+val+')'
				elif operation == 'between':
					if isinstance(v, tuple) or isinstance(v, list) and len(v) == 2:
						val = v
					else:
						assert False, "Value should be list or tuple of length 2."
				else:
					val = str(v)
				if query:
					query = query + ' AND ' + SqliteAdapter.operations[operation].format(field=field, val=val)
				else:
					query = SqliteAdapter.operations[operation].format(field=field, val=val)
		return query

	def get_exec(self, table, **kwargs):
		where_clause =  self._prepare_where_string(**kwargs)
		query = self.select_frame.format(table = table.lower(), clause = where_clause)
		return query
		raise NotImplementedError('Operation not supported by adapter')

class Orm(Query):
	def __init__(self, database, **kwargs):
		super(Orm, self).__init__(database)
	
	def filter(self, **kwargs):
		return self.get_exec(self.__class__.__name__, **kwargs)
	
	def get(self, **kwargs):
		pass

	def all(self):
		pass

