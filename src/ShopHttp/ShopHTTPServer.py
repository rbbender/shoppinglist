from http.server import HTTPServer
from .Router import Router
from .RequestHandler import RequestHandler

class ShopHTTPServer(HTTPServer, Router):
    def __init__(self, server_address):
        Router.__init__(self)
        HTTPServer.__init__(self, server_address=server_address, RequestHandlerClass=RequestHandler)


