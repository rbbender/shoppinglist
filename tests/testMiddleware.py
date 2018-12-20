import unittest
from unittest.mock import Mock
import io

from ShopHttp.middleware import parse_json_body
from ShopHttp.RequestHandler import RequestHandler


class TestJsonMiddleware(unittest.TestCase):
    def test_parse_json_body(self):
        test_msg = b"""{"test":"test"}\r"""
        hndl = Mock(RequestHandler)
        hndl.headers = {"Content-Type": "application/json", "Content-Length": "16"}
        hndl.rfile = io.BytesIO(test_msg)
        parse_json_body(hndl)
        self.assertEqual({"test": "test"}, hndl.json_body, "Incorrect parsing of application/json body")

    def test_parse_json_body_not_json(self):
        test_msg = b"""{"test":"test"}\r"""
        hndl = Mock(RequestHandler)
        hndl.headers = {"Content-Type": "application/hhh", "Content-Length": "16"}
        hndl.rfile = io.BytesIO(test_msg)
        parse_json_body(hndl)
        self.assertFalse(hasattr(hndl, "json_body"), "Non json Content-Type adds json_body to handler")

    def test_parse_json_body_zero_length(self):
        test_msg = b"""{"test":"test"}\r"""
        hndl = Mock(RequestHandler)
        hndl.headers = {"Content-Type": "application/json", "Content-Length": "0"}
        hndl.rfile = io.BytesIO(test_msg)
        parse_json_body(hndl)
        self.assertFalse(hasattr(hndl, "json_body"), "Zero-length json body Content-Type adds json_body to handler")
