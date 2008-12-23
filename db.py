class Relation:
    pass

class Field:
    def __init__(self, name, text, alias = None):
        self.name = name
        self.text = text
        self.alias = alias or self.name

    
