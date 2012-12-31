# Author : Shabinesh <shabi@fossix.org>

# Desc : This file is the SQL generation core.

from .adapters import Adapter

def spacecat(*args):
    return ' '.join(list(args))

_surround = lambda x, start, end: ''.join([start,x,end])


class Child:

    def __init__(self, name, value, relation):
        self.sub_tree = False
        if value.__class__.__name__ == 'Table':
            self.sub_tree = True
            self.name = name
            self.relation = relation
            self.value = value
            return

        if relation in Adapter.operations:
            self.relation = Adapter.operations[relation]
        else:
            assert False, "Invalid operation :{0}".format(relation)
        
        if relation == 'between':
            if type(value) in (list, tuple):
                self.q = spacecat(name, self.relation.format(value[0], value[1]))
            else:
                assert False, "should be a tuple or list"
        elif relation == 'in':
            self.q = spacecat(name, Adapter.operations[relation], ','.join([_surround(str(i),'"', '"') for i in value]))
        else:
            self.q = spacecat(name, Adapter.operations[relation], str(value))
        
    
    def get_c(self):
        return self.q
            

class Tree:
    """ Tree"""
    _connectors = ('AND', 'OR')
    _quantifier = 'DISTINCT'

    def __init__(self, table):
        self.t = []
        self.table = table
        self.distinct_f = False

    def create_select(self):
        d = self._quantifier if self.distinct_f else ''
        select_fields = '*' if not self.select_fields else ', '.join(self.select_fields)
        self.template = "SELECT {0} {1} FROM {2}".format(d, select_fields, self.table)
        
    def parse_and_add(self, select=[], **kwargs):
        for s, v in kwargs.items():
            if '__' in s:
                name, relation  = s.split('__')
            else:
                name, relation = s, 'eq'
            self.add(name, v, relation)

        self.select_fields = select if select else None

    def add(self, name, value, relation, connector='AND'):
        assert connector in self._connectors, "'{0}' is not valid connector".format(connector)
        child = Child(name, value, relation)
        self.t.append((connector, child))
        return

    def get_sql(self):
        query = ''
        self.create_select()
        t = sorted(self.t, key=lambda o: 1 if o[1].__class__.__name__ == 'Table' else 0)
        for c, obj in self.t:
            if not obj.sub_tree:
                query = spacecat(query, obj.get_c(), c)
            else:
                query += spacecat(obj.name, obj.relation, '(', obj.value.filter(obj.name).sql(), ')')                
        if query.rsplit(' ',1)[0] == 'AND': query = query.rsplit(' ',1)[0] + ' '
        where_clause = '' if query == '' else 'WHERE'
        return spacecat(self.template, where_clause, query) #.rsplit(' ',1)[0]

        


