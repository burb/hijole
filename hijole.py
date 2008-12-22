from wsgiref.simple_server import make_server

import cgi
import logging

logging.basicConfig(level = logging.INFO)

def response(path_info):
    components = [c for c in path_info.split('/') if c != ""]
    module_path = '.'.join(components[:-1])
    function = components[-1]
    try:
        module = __import__(module_path)
        reload(module)
        if function in module.__dict__:
            f = module.__dict__[function]
            if f.func_code.co_argcount == 0:
                return f()
            else:
                return f(path_info)
    except Exception, e:
        return "error: %s" % str(e)
    
    

def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/html"), ("Encoding", "utf-8")])
    return response(environ.get("PATH_INFO"))

httpd = make_server("localhost", 8888, app)
print("starting serve on 8888 ...")
httpd.serve_forever()
