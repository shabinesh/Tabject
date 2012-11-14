

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
		raise NotImplementedError('Adapter not avaliable, specify one of {adpters}'.format(adapters=self.avaliable_adapters.keys()))

	def connect(self, *args, **kwargs):
		raise NotImplementedError('Implement in subclass.')

class SqliteAdapter(Adapter):
    __dbname__ = 'sqlite3'
    __affinity__ = {
            ('int',
             'integer',
             'tinyint',
             'smallint',
             'mediumint',
             'bigint',
             'unsigned big int',
             'int2',
             'int8',
             'numeric',): Integer,
            ('character',
             'varchar',
             'text',
             'nvarchar',
             'nchar',
             'varying character',
             'native character',
             'clob',): Text,
            ('real',
             'double',
             'double precision',
             'float',
             'decimal',): Real,
            ('boolean',): Bool,
            ('date',
             'date time',): Date,
            }

    def __init__(self, database, **kwargs):
        sqlite = self.import_a(SqliteAdapter.__dbname__)
        self.operations = {
                'ieq' : 'LIKE %(v)s ESCAPE',
                'icontains' : 'GLOB %(v)s',
                'istartswith' : 'LIKE %(v)s ESCAPE',
                'startwith' : 'GLOB %(v)s'
                }.update(Adapter.operations)
	self._connection = sqlite.connect(database, **kwargs)
        self._cursor = self._connection.cursor()

    def execute(self, sql):
        return self._cursor.execute(sql)
    
    @staticmethod
    def _gettype(t):
        for f, ty in SqliteAdapter.__affinity__.items():
            if t.lower() in f:
                return ty
        return Text

    def get_columns_and_types(self, table):
        return {r[1]:self._gettype(r[2]) for r in self.execute('PRAGMA table_info("{0}")'.format(table))}
