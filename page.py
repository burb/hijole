import logging

def page(f):
    'turn function f into Page object'
    page = Page()
    page.set_handler(f)
    return page

class Page:
    def __init__(self):
        pass

    def set_handler(self, handler):
        self.handler = handler
    
    def __call__(self, *args):
        print "kuku"
        if self.handler.func_code.co_argcount == 0:
            return self.handler()
        else:
            return self.handler(*args)
    
    
    
