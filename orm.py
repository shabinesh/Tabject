from .exceptions import ImproperlyConfigured
from .tree import Tree
import sqlite3

class MkTableObj(type):
    @classmethod
    def _affinity(klass, **kwargs, adapter):
        for f, t in kwargs:
            klass._fields[field] = adapter.get_type(f)()

    def __init__(klass, table, (Orm), **kwargs, adapter):
        def setattr(self, f, v):
            if f in self._fields:
                self._fields[f] = 
    
        def getattribute(self, f):
            if f in self._fields:
                return self._fields[f]
            raise AttributeError
        
        klass.__table__ = table
        klass._fields = self._affinity(kwargs, adapter)

class Database:
    def __init__(self, database, adapter = sqlite3):
        self._table_cache = dict
        if adapter.__name__ == 'sqlite3':
            self.adapter = SqliteAdapter()
        elif adapter.__name__ == 'mysql':
            # similar for mysql and postgresql
            pass

    def execute(self, q):
        # A adapter should always return a cursor object
        self.adapter.cursor.execute(q)

    def connect(self):
        return self.adapter.connect()
	
    def execute(self, query):
        pass
    
    @staticmethod
    def _mkclass(table):


        l = self.adapter.get_columns_and_types(table)
        obj = type(table, (Orm), {'_fields':l})

    def __getattr__(self, name):
        if name in self._table_cache:
            return self._table_cache.get(name)
        #create the object and add it to _table_cache and return instance of it.

class Orm():
    def __init__(self, database, **kwargs):
        super(Orm, self).__init__(database)
                
    def filter(self, **kwargs):
        return self.get_exec(self.__class__.__name__, **kwargs)
	
    def get(self, **kwargs):
        pass

    def all(self):
        pass

