from collections import OrderedDict

class Router(object):
    def __init__(self):
        self.handlers = {"GET": OrderedDict(),
                         "POST": OrderedDict(),
                         "PATCH": OrderedDict(),
                         "DELETE": OrderedDict()}

    def get_handlers_method(self, method):
        return self.handlers.get(method, None)

    def add_handler(self, method, path, handler):
        hndls = self.get_handlers_method(method)
        hndls[path] = handler

    def _match_path(self, method, path):
        hndls = self.get_handlers_method(method)
        splitted_path = path.strip('/ ').split('/')
        for k in hndls:
            params = {}
            splitted_k = k.strip('/ ').split('/')
            if len(splitted_path) == len(splitted_k):
                for ii in range(len(splitted_path)):
                    sg = splitted_k[ii]
                    if len(sg) and sg[0] == '{' and sg[-1] == '}':
                        params[sg[1:-1]] = splitted_path[ii]
                    else:
                        if sg != splitted_path[ii]:
                            break
                else:
                    return hndls[k], params
        return None, {}

    def get_handler(self, method, path):
        hndls = self.get_handlers_method(method)
        hnd = hndls.get(path, None)
        if hnd is not None:
            return hnd, {}
        return self._match_path(method, path)
