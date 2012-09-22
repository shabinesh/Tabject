Tabject
=======

A database table to object, | a striped down fast python ORM.

Usage
======
```
>>> from Tabject.orm import Orm

>>> o = Orm(database = "mydb")

>>> o.filter(name__eq = 'Shabinesh', age__gte = 24, hip_size__in = [30,32,34])
```
