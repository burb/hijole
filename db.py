from collections import defaultdict

import pickle

class Meta(type):
    def __init__(self, name, superclasses, dict):
        print("HA!")
        type.__init__(self, name, superclasses, dict)
        self.primary_key = []
        for name, element in dict.iteritems():
            if isinstance(element, Element):
                element.name = name
                element.relation = self
                if element.primary_key:
                    self.primary_key.append(element.name)

class Element(object):
    def create(self):
        raise NotImplementedError("My subclass must define create method")

    def update(self, old):
        raise NotImplementedError("My subclass must define update method")

    def delete(self):
        raise NotImplementedError("My subclass must define delete method")

    def relation_name(self):
        return self.relation.__name__

class Relation(object):
    __metaclass__ = Meta

    @classmethod
    def create(cls):
        columns = []
        for name, value in cls.__dict__.iteritems():
            if isinstance(value, Element):
                columns.append(value.create())
        return "CREATE TABLE %s (%s %s);" % (cls.__name__,
                                             ', '.join(columns),
                                             ", PRIMARY KEY (%s)" % ', '.join(cls.primary_key) if cls.primary_key != [] else "")
    @classmethod
    def save_to_db(cls, cursor):
        d = {}
        for k, v in cls.__dict__.iteritems():
            d[k] = v
        cursor.execute("INSERT INTO HijoleRelations (relation_name, relation_pickle) VALUES (%s, %s)",
                       (cls.__name__, pickle.dumps(d)))

    @classmethod
    def last_from_db(cls, cursor):
        cursor.execute("SELECT relation_pickle FROM HijoleRelations WHERE relation_name = %s ORDER BY relation_update_time DESC",
                       (cls.__name__,))
        result = cursor.fetchone()
        if result != None:
            d = pickle.loads(result[0])
            return Meta(cls.__name__, (Relation,), d)
        else:
            return None
    
    @classmethod
    def element_iterator(cls):
        for element in cls.__dict__.itervalues():
            if isinstance(element, Element):
                yield element

    @classmethod
    def delete(cls):
        return "DROP TABLE %s" % cls.__name__

    @classmethod
    def update(cls, old):
        result = []
        new_elements = set(cls.element_iterator())
        old_elements = set(old.element_iterator())
        if old.primary_key != cls.primary_key:
            if old.primary_key != []:
                result.append("ALTER TABLE %(name)s DROP CONSTRAINT %(name)s_pkey" % {'name': cls.__name__})
            result.append("ALTER TABLE %s ADD PRIMARY KEY (%s)" % (cls.__name__, ', '.join(cls.primary_key)))
        changes = defaultdict(lambda: ColumnChange(None, None))
        for new in new_elements:
            changes[new.name].new = new
        for old in old_elements:
            changes[old.name].old = old
        for name, change in changes.iteritems():
            old, new = change.old, change.new
            if old == None:
                result.append("ALTER TABLE %s ADD COLUMN %s" % (cls.__name__, new.create()))
            elif new == None:
                result.append("ALTER TABLE %s %s" % (cls.__name__, old.delete()))
            elif new != None and old != None and not new.equal_to(old):
                result.extend(new.update(old))
            elif new == None and old == None:
                raise Exception("new and old can't be both None")
        return ";".join(result + [""])
            
class ColumnChange:
    def __init__(self, old, new):
        self.old = old
        self.new = new
        
class PrimaryKey(Element):
    def __init__(self, *columns):
        self.columns = columns

    def create(self, *args):
        return "PRIMARY KEY (%s)" % ', '.join(self.columns)

class Column(Element):
    # todo!! add constraints and checks
    def __init__(self, type, default = None, can_be_null = False, primary_key = False):
        self.type = type
        self.default = default
        self.can_be_null = can_be_null
        self.primary_key = primary_key

    def escaped_default(self):
        if type(self.default) == str:
            return "'%s'" % self.default
        else:
            return self.default

    def create(self):
        return "%s %s %s %s" % (self.name, self.type, "DEFAULT %s" % self.default if self.default != None else "", "NOT NULL" if self.can_be_null == False else "")

    def equal_to(self, other):
        return self.type == other.type and self.default == other.default and self.can_be_null == other.can_be_null and self.primary_key == other.primary_key

    # todo!! remove duplication
    def update(self, other):
        result = []
        if self.type != other.type:
            result.append("ALTER TABLE %s ALTER COLUMN %s TYPE %s" % (self.relation_name(), self.name, self.type))
        if self.default != other.default:
            if self.default == None:
                result.append("ALTER TABLE %s ALTER COLUMN %s DROP DEFAULT" % (self.relation_name(), self.name))
            else:
                result.append("ALTER TABLE %s ALTER COLUMN %s SET DEFAULT %s" % (self.relation_name(), self.name, self.escaped_default()))
        if self.can_be_null != other.can_be_null:
            if self.can_be_null == True:
                result.append("ALTER TABLE %s ALTER COLUMN %s DROP NOT NULL" % (self.relation_name(), self.name))
            else:
                result.append("ALTER TABLE %s ALTER COLUMN %s SET NOT NULL" % (self.relation_name(), self.name))
        return result

    def delete(self):
        return "DROP COLUMN %s" % self.name

class TextColumn(Column):
    def __init__(self, **kwargs):
        Column.__init__(self, type = "TEXT", **kwargs)
        
class VarCharColumn(Column):
    def __init__(self, length = 255, **kwargs):
        Column.__init__(self, "VARCHAR(%d)" % length, **kwargs)

class TimestampColumn(Column):
    def __init__(self, **kwargs):
        Column.__init__(self, type = 'TIMESTAMP', **kwargs)

class ReferenceColumn(Column):
    def __init__(self, reference, **kwargs):
        Column.__init__(self, None, **kwargs)
        self.reference = reference

    def create(self):
        return "%s REFERENCES %s(%s)" % (self.name, self.reference.relation.__name__, self.reference.name)

def relation_exists(relation_name, cursor):
    return cursor.execute("SELECT * FROM pg_tables WHERE tablename = %s", (relation_name,)) != 0
