class Relation(object):
    @classmethod
    def create(cls):
        columns = []
        for name, value in cls.__dict__.iteritems():
            if isinstance(value, Element):
                columns.append(value.create(name))
        return "CREATE TABLE %s (%s);" % (cls.__name__, ', '.join(columns))
        

class Element(object):
    def create(self, name):
        raise NotImplementedError("My subclass must define create method")

    def update(self, old, name):
        raise NotImplementedError("My subclass must define update method")

    def delete(self, name):
        raise NotImplementedError("My subclass must define delete method")

class Column(Element):
    def __init__(self, definition):
        self.definition = definition

    def create(self, name):
        return "%s %s" % (name, self.definition)
