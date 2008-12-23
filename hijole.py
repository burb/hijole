from wsgiref.simple_server import make_server

import cgi
import logging
import traceback
import types

logging.basicConfig(level = logging.INFO)

def recursive_reload(module, known = None):
    if type(module) != types.ModuleType or (known != None and module in known):
        return
    if known == None:
        known = {}
    known[module] = True
    for name, m in module.__dict__.iteritems():
        recursive_reload(m, known)
    reload(module)

def response(environ, path_info):
    components = [c for c in path_info.split('/') if c != ""]
    if len(components) == 0:
        return "hijole!"
    module_path = '.'.join(components[:-1])
    function = components[-1]
    try:
        module = __import__(module_path)
        # recursive_reload(module)
        reload(module)
        if function in module.__dict__:
            f = module.__dict__[function]
            if type(f) == types.FunctionType:
                if f.func_code.co_argcount == 0:
                    return f()
                else:
                    return f(environ)
            else:
                return f(environ)
        else:
            return "please define function %s" % function
    except Exception, e:
        return "error: %s" % traceback.format_exc().replace('\n', '<br/>')
    
    

def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/html"), ("Encoding", "utf-8")])
    return response(environ, environ.get("PATH_INFO"))

httpd = make_server("localhost", 8888, app)
print("starting serve on 8888 ...")
httpd.serve_forever()
