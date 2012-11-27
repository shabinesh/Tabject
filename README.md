Tabject
=======

A database table to object, | a striped down fast python ORM. Django style orm operations.

Tabject is in it's very very very early stage.

The idea of `Tabject` is to plug in Tabject into any application not using ORM, but wants to
update their code base to eliminate hard coded SQL and use ORM style operation for data access. 

Tabject supports only DML operations which means you immense flexibility and control over schema.

since Tabject dynamically creates table objects when needed, any change in the table structure 
get reflected on a application restart. See the below example:

Usage
======
```
>>> from Tabject.orm import Orm

>>> db = Database("dev.db")

>>> users = db.user_table

>>> users.filter(name__eq = 'Shabinesh', age__gte = 24, hip_size__in = [30,32,34])

```

Easy isn't it?
