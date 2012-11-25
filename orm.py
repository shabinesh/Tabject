from .exceptions import ImproperlyConfigured
from .tree import Tree
from .adapters import *
import sqlite3

""""
class MkTableObj:
    @staticmethod
    def _affinity(klass, adapter, **kwargs):
        for f, t in kwargs:
            klass._fields[field] = adapter.get_type(f)()

    def __init__(self, table, bases, adapter, kwargs):
        klass = type(table, bases, {})
        def setattr(self, f, v):
            if f in self._fields:
                self._fields[f] = v #change value to type
    
        def getattribute(self, f):
            if f in self._fields:
                return self._fields[f]
            raise AttributeError
        
        klass.__setattr__ = setattr
        klass.__getattribute__ = getattribute
        klass.__table__ = table
        klass._fields = MkTableObject._affinity(adapter, kwargs)

"""

class Database:
    def __init__(self, database_name, adapter='sqlite3'):
        self._table_cache = {}
        if adapter == 'sqlite3':
            self.adapter = SqliteAdapter(database_name)
        elif adapter == 'mysql':
            # similar for mysql and postgresql
            pass

    def execute(self, q):
        # A adapter should always return a cursor object
        self.adapter.cursor.execute(q)

    def connect(self):
        return self.adapter.connect()
    
    def _mkclass(self, table):
        print "create,", table
        l = self.adapter.get_columns_and_types(table)
        obj = type(table, (Orm, ), {'_fields':l.keys()})
        return obj

    def __getattr__(self, name):
        print "get, ", name
        if name in self.__dict__:
            return self.__dict__[name]
        if name in self._table_cache:
            return self._table_cache.get(name)
        t = self._mkclass(name)
        print "t :", t
        self._table_cache[name] = t
        return t()
        #create the object and add it to _table_cache and return instance of it.

class Orm(object):
               
    def filter(self, **kwargs):
        return self.get_exec(self.__class__.__name__, **kwargs)
	
    def get(self, **kwargs):
        pass

    def all(self):
        pass

