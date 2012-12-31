from .exceptions import ImproperlyConfigured
from .tree import Tree
from .adapters import *
import sqlite3
import json

class TableMeta(type):
    def __init__(klass, *args, **kwargs):
        def getattr(self, n):
            if n in self._fields:
                return n
            raise AttributeError('{0} not a table field'.format(n))

        setattr(klass, '__getattr__', getattr)
        super(TableMeta, klass).__init__(*args, **kwargs)

class Database:
    def __init__(self, database_name, adapter='sqlite3'):
        self.__dbname__ = database_name
        self._table_cache = {}
        if adapter == 'sqlite3':
            self.adapter = SqliteAdapter(database_name)
        elif adapter == 'mysql':
            # similar for mysql and postgresql
            pass

    def execute(self, q):
        # A adapter should always return a cursor object
        return self.adapter.execute(q)

    def connect(self):
        return self.adapter.connect()
    
    def _mkclass(self, table):
        l = self.adapter.get_columns_and_types(table)

        class Table(Orm):
            _fields = tuple([i[0] for i in l])
            db = self
            __table__ = table
            __metaclass__ = TableMeta
            
            def __repr__(self):
                return "<Table instance '%s'>" % self.__table__

        return Table

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        if name in self._table_cache:
            return self._table_cache.get(name)()
        t = self._mkclass(name)
        self._table_cache[name] = t
        return t()
        #create the object and add it to _table_cache and return instance of it.

    def __repr__(self):
        return "<database {0} instance>".format(self.__dbname__)
        
class Orm(object):

    def __init__(self):
        self.tree = Tree(self.__table__)
        
    def filter(self,*args, **kwargs):
        self.tree.parse_and_add(select=args, **kwargs)
        return self
	
    def get(self, **kwargs):
        pass

    def all(self):
        return self
        return self.filter()
    
    def distinct(self):
        self.tree.distinct_f = True
        return self

    def sql(self):
        return self.tree.get_sql()

    def x(self):
        print self.sql()
        return self.db.execute(self.sql())

    def JSON(self):
        return json.dumps([dict(zip(self._fields, item)) for item in self.x()])
        
        
        
    
        
        
