from .exceptions import ImproperlyConfigured
from .tree import Tree


class Database:
    def __init__(self, adapter = None):
        assert adapter, "Empty adapter !!!"
        self.adapter = adapter

    def connect(self):
        return self.adapter.connect()
	
    def execute(self, query):
        pass

class Query(object):
    def __init__(self, database):
	#TO-DO pick right adapter according to database.
        self.tree = Tree('table')

    def get_exec(self, table, **kwargs):
        tree = Tree(table)
        tree.parse_and_add(**kwargs)
        return tree.get_sql()

class Orm(Query):
    def __init__(self, database, **kwargs):
        super(Orm, self).__init__(database)
                
    def filter(self, **kwargs):
        return self.get_exec(self.__class__.__name__, **kwargs)
	
    def get(self, **kwargs):
        pass

    def all(self):
        pass

