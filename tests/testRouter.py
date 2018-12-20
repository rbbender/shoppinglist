import unittest
from ShopHttp import Router

supported_http_methods = ["GET", "POST", "PATCH", "DELETE"]

class RouterTestCase(unittest.TestCase):
    def test_initial_state(self):
        router = Router()
        for method in supported_http_methods:
            self.assertEqual(0, len(router.get_handlers_method(method)), f"There supposed to be 0 handlers for {method}")

    def test_add_handler_static(self):
        testHandlerRoot1 = lambda hndl: "GET /"
        testHandlerRoot2 = lambda hndl: "POST /"
        testHandlerRoot3 = lambda hndl: "PATCH /"
        testHandlerRoot4 = lambda hndl: "DELETE /"
        testHandler1 = lambda hndl: "GET"
        testHandler2 = lambda hndl: "GET"
        testHandler3 = lambda hndl: "POST"
        testHandler4 = lambda hndl: "POST"
        testHandler5 = lambda hndl: "PATCH"
        testHandler6 = lambda hndl: "PATCH"
        testHandler7 = lambda hndl: "DELETE"
        testHandler8 = lambda hndl: "DELETE"
        router = Router()
        router.add_handler('GET',   '/static/handler1', testHandler1)
        router.add_handler('GET',   '/static/handler2', testHandler2)
        router.add_handler('POST',  '/static/handler1', testHandler3)
        router.add_handler('POST',  '/static/handler2', testHandler4)
        router.add_handler('PATCH', '/static/handler1', testHandler5)
        router.add_handler('PATCH', '/static/handler2', testHandler6)
        router.add_handler('DELETE', '/static/handler1', testHandler7)
        router.add_handler('DELETE', '/static/handler2', testHandler8)
        router.add_handler('GET', '/', testHandlerRoot1)
        router.add_handler('POST', '/', testHandlerRoot2)
        router.add_handler('PATCH', '/', testHandlerRoot3)
        router.add_handler('DELETE', '/', testHandlerRoot4)
        self.assertEqual((testHandler1, {}), router.get_handler("GET", '/static/handler1'), "Wrong GET handler1")
        self.assertEqual((testHandler2, {}), router.get_handler("GET", '/static/handler2'), "Wrong GET handler2")
        self.assertEqual((testHandler3, {}), router.get_handler("POST", '/static/handler1'), "Wrong POST handler1")
        self.assertEqual((testHandler4, {}), router.get_handler("POST", '/static/handler2'), "Wrong POST handler2")
        self.assertEqual((testHandler5, {}), router.get_handler("PATCH", '/static/handler1'), "Wrong PATCH handler1")
        self.assertEqual((testHandler6, {}), router.get_handler("PATCH", '/static/handler2'), "Wrong PATCH handler2")
        self.assertEqual((testHandler7, {}), router.get_handler("DELETE", '/static/handler1'), "Wrong DELETE handler1")
        self.assertEqual((testHandler8, {}), router.get_handler("DELETE", '/static/handler2'), "Wrong DELETE handler2")
        self.assertEqual((testHandlerRoot1, {}), router.get_handler("GET", '/'), "Wrong GET / handler")
        self.assertEqual((testHandlerRoot2, {}), router.get_handler("POST", '/'), "Wrong POST / handler")
        self.assertEqual((testHandlerRoot3, {}), router.get_handler("PATCH", '/'), "Wrong PATCH / handler")
        self.assertEqual((testHandlerRoot4, {}), router.get_handler("DELETE", '/'), "Wrong DELETE / handler")

    def test_get_handler_none_handlers_empty(self):
        router = Router()
        self.assertEqual((None, {}), router.get_handler("GET", "/static/handler1"),
                         "Wrong return on non-existing GET handler")
        self.assertEqual((None, {}), router.get_handler("POST", "/static/handler1"),
                         "Wrong return on non-existing POST handler")
        self.assertEqual((None, {}), router.get_handler("PATCH", "/static/handler1"),
                         "Wrong return on non-existing PATCH handler")
        self.assertEqual((None, {}), router.get_handler("DELETE", "/static/handler1"),
                         "Wrong return on non-existing DELETE handler")
        self.assertEqual((None, {}), router.get_handler("GET", "/param/{paramName}"),
                         "Wrong return on non-existing GET handler")
        self.assertEqual((None, {}), router.get_handler("POST", "/param/{paramName}"),
                         "Wrong return on non-existing POST handler")
        self.assertEqual((None, {}), router.get_handler("PATCH", "/param/{paramName}"),
                         "Wrong return on non-existing PATCH handler")
        self.assertEqual((None, {}), router.get_handler("DELETE", "/param/{paramName}"),
                         "Wrong return on non-existing DELETE handler")

    def test_get_handler_none_static_handlers(self):
        router = Router()
        testHandler1 = lambda hndl: "GET"
        testHandler2 = lambda hndl: "POST"
        testHandler3 = lambda hndl: "PATCH"
        testHandler4 = lambda hndl: "DELETE"
        router.add_handler("GET", '/static/handler1', testHandler1)
        router.add_handler("POST", '/static/handler1', testHandler2)
        router.add_handler("PATCH", '/static/handler1', testHandler3)
        router.add_handler("DELETE", '/static/handler1', testHandler4)
        self.assertEqual((None, {}), router.get_handler("GET", "/static/handler2"),
                         "Supposed to return (None, {}) for non-existing handler")
        self.assertEqual((None, {}), router.get_handler("POST", "/static/handler2"),
                         "Supposed to return (None, {}) for non-existing handler")
        self.assertEqual((None, {}), router.get_handler("PATCH", "/static/handler2"),
                         "Supposed to return (None, {}) for non-existing handler")
        self.assertEqual((None, {}), router.get_handler("DELETE", "/static/handler2"),
                         "Supposed to return (None, {}) for non-existing handler")

    def test_get_handler_parameters_precedence(self):
        router = Router()
        testHandler1 = lambda hndl: "GET"
        testHandler2 = lambda hndl: "POST"
        testHandler3 = lambda hndl: "PATCH"
        testHandler4 = lambda hndl: "DELETE"
        testHandler5 = lambda hndl: "GET"
        testHandler6 = lambda hndl: "POST"
        testHandler7 = lambda hndl: "PATCH"
        testHandler8 = lambda hndl: "DELETE"
        router.add_handler("GET", "/", lambda handler: "TEST")
        router.add_handler("GET", "/parameters/{param2}", testHandler5)
        router.add_handler("POST", "/parameters/{param2}", testHandler6)
        router.add_handler("PATCH", "/parameters/{param2}", testHandler7)
        router.add_handler("DELETE", "/parameters/{param2}", testHandler8)
        router.add_handler("GET", "/{param1}", testHandler1)
        router.add_handler("POST", "/{param1}", testHandler2)
        router.add_handler("PATCH", "/{param1}", testHandler3)
        router.add_handler("DELETE", "/{param1}", testHandler4)
        self.assertEqual((testHandler1, {"param1": "getHandler"}), router.get_handler("GET", "/getHandler"),
                         "Wrong handler/parsed params for GET parameter-based route")
        self.assertEqual((testHandler2, {"param1": "postHandler"}), router.get_handler("POST", "/postHandler"),
                         "Wrong handler/parsed params for POST parameter-based route")
        self.assertEqual((testHandler3, {"param1": "patchHandler"}), router.get_handler("PATCH", "/patchHandler"),
                         "Wrong handler/parsed params for PATCH parameter-based route")
        self.assertEqual((testHandler4, {"param1": "deleteHandler"}), router.get_handler("DELETE", "/deleteHandler"),
                         "Wrong handler/parsed params for DELETE parameter-based route")
        self.assertEqual((testHandler5, {"param2": "getHandler"}), router.get_handler("GET", "/parameters/getHandler"),
                         "Wrong handler/parsed params for GET parameter-based route")
        self.assertEqual((testHandler6, {"param2": "postHandler"}), router.get_handler("POST", "/parameters/postHandler"),
                         "Wrong handler/parsed params for POST parameter-based route")
        self.assertEqual((testHandler7, {"param2": "patchHandler"}), router.get_handler("PATCH", "/parameters/patchHandler"),
                         "Wrong handler/parsed params for PATCH parameter-based route")
        self.assertEqual((testHandler8, {"param2": "deleteHandler"}), router.get_handler("DELETE", "/parameters/deleteHandler"),
                         "Wrong handler/parsed params for DELETE parameter-based route")



if __name__ == '__main__':
    unittest.main()
