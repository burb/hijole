import cgi
import logging

def page(f):
    'turn function f into Page object'
    page = Page()
    page.set_handler(f)
    return page

def simple(f):
    def result(environ):
        request = Request(environ)
        return f(**request.params)
    return result

def typed(**types):
    def decorator(f):
        def result(environ):
            request = Request(environ, types)
            return f(**request.params)
        return result
    return decorator

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

class Request:
    def __init__(self, environ, types = {}):
        qs = environ.get("QUERY_STRING")
        params = cgi.parse_qs(qs)
        for x in params:
            params[x] = types[x](params[x][0]) if x in types else params[x][0]
        self.params = params
    
    
