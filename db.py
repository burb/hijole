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

        
class PrimaryKey(Element):
    def __init__(self, *columns):
        self.columns = columns

    def create(self, *args):
        return "PRIMARY KEY (%s)" % ', '.join(self.columns)

class Column(Element):
    def __init__(self, type, default = None, can_be_null = False, primary_key = False):
        self.type = type
        self.default = default
        self.can_be_null = can_be_null
        self.primary_key = primary_key

    def create(self):
        return "%s %s %s %s" % (self.name, self.type, "DEFAULT %s" % self.default if self.default != None else "", "NOT NULL" if self.can_be_null == False else "")

class TextColumn(Column):
    def __init__(self, **kwargs):
        Column.__init__(self, type = "TEXT", **kwargs)
        
class VarCharColumn(Column):
    def __init__(self, length = 255, **kwargs):
        Column.__init__(self, "VARCHAR(%d)" % length, **kwargs)

class ReferenceColumn(Column):
    def __init__(self, reference, **kwargs):
        Column.__init__(self, None, **kwargs)
        self.reference = reference

    def create(self):
        return "%s REFERENCES %s(%s)" % (self.name, self.reference.relation.__name__, self.reference.name)

    
