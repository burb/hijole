import page

def hi():
    return "kuku"

@page.simple
def ho(name):
    return "hi %s" % name

@page.typed(x = int, y = int)
def plus(x, y):
    return "%d + %d = %d" % (x, y, x + y)
