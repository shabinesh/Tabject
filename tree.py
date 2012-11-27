from .adapters import Adapter

def spacecat(*args):
    return ' '.join(list(args))

_surround = lambda x, start, end: ''.join([start,x,end])


class Child:

    def __init__(self, name, value, relation):
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

    def __init__(self, table, field=None):
        self.field = field if field else '*'
        self.t = []
        self.template = "SELECT {0} FROM {1}".format(self.field, table)
        
    def parse_and_add(self, **kwargs):
        for s, v in kwargs.items():
            name, relation  = s.split('__')
            self.add(name, v, relation)

    def add(self, name, value, relation, connector='AND'):
        assert connector in self._connectors, "'{0}' is not valid connector".format(connector)
        if type(value) in (int, str, list, tuple):
            child = Child(name, value, relation)
            self.t.append((connector, child))
        else:
            self.t.append((relation, value))
        return
    
    def _is_child(self, c):
        if isinstance(c, Child):
            return True
        return False

    def get_sql(self):
        query = ''
        for c, obj in self.t:
            if isinstance(obj, Child):
                query = spacecat(query, obj.get_c(), c)
            elif isinstance(obj, Tree):
                query = _surround(obj.get_sql(), '(', ')')
        return spacecat(self.template, 'WHERE', query).rsplit(' ',1)[0]

        


