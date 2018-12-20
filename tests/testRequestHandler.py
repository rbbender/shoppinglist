from io import BytesIO
from unittest import TestCase
from unittest.mock import Mock, patch
from email import policy
from email.parser import BytesParser
from email.contentmanager import raw_data_manager
import json

import functools

from ShopHttp import RequestHandler, ShopHTTPServer
from socket import socket

import socketserver



class TestRequestHandler(TestCase):
    def test_RequestHandler_post_json(self):
        test_request_post_json = b"""POST / HTTP/1.1\r
Accept: */*\r
Accept-Encoding: gzip, deflate, br\r
Accept-Language: en-US,en;q=0.9\r
Connection: keep-alive\r
Content-Length: 16\r
content-type: application/json\r
Host: localhost:8000\r
Origin: null\r
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36\r
\r
{"test":"test"}
\r
"""
        mock_sock = Mock(socket)
        mock_sock.recv.return_value = test_request_post_json
        mock_sock.makefile.return_value = BytesIO(test_request_post_json)
        mock_serv = Mock(ShopHTTPServer)
        mock_serv.get_handler.return_value = (lambda hndl: None, {})
        hndl = RequestHandler(mock_sock, ("localhost", 8080), mock_serv)
        self.assertTrue(hasattr(hndl, "json_body"), "No parsed JSON in handler json_body parameter")
        self.assertEqual({"test": "test"}, hndl.json_body, "Incorrect json body parsing")

    def test_RequestHandler_patch_json(self):
        test_request_post_json = b"""PATCH / HTTP/1.1\r
Accept: */*\r
Accept-Encoding: gzip, deflate, br\r
Accept-Language: en-US,en;q=0.9\r
Connection: keep-alive\r
Content-Length: 16\r
content-type: application/json\r
Host: localhost:8000\r
Origin: null\r
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36\r
\r
{"test":"test"}
\r
"""
        mock_sock = Mock(socket)
        mock_sock.recv.return_value = test_request_post_json
        mock_sock.makefile.return_value = BytesIO(test_request_post_json)
        mock_serv = Mock(ShopHTTPServer)
        mock_serv.get_handler.return_value = (lambda hndl: None, {})
        hndl = RequestHandler(mock_sock, ("localhost", 8080), mock_serv)
        self.assertTrue(hasattr(hndl, "json_body"), "No parsed JSON in handler json_body parameter")
        self.assertEqual({"test": "test"}, hndl.json_body, "Incorrect json body parsing")

    def test_RequestHandler_get_json(self):
        test_request_post_json = b"""GET / HTTP/1.1\r
Accept: */*\r
Accept-Encoding: gzip, deflate, br\r
Accept-Language: en-US,en;q=0.9\r
Connection: keep-alive\r
Content-Length: 0\r
content-type: application/json\r
Host: localhost:8000\r
Origin: null\r
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36\r
\r
\r
"""
        mock_sock = Mock(socket)
        mock_sock.recv.return_value = test_request_post_json
        mock_sock.makefile.return_value = BytesIO(test_request_post_json)
        mock_serv = Mock(ShopHTTPServer)
        mock_serv.get_handler.return_value = (lambda hndl: None, {})
        hndl = RequestHandler(mock_sock, ("localhost", 8080), mock_serv)
        self.assertFalse(hasattr(hndl, "json_body"), "handler json_body parameter in GET request")

    def test_RequestHandler_delete_json(self):
        test_request_post_json = b"""DELETE / HTTP/1.1\r
Accept: */*\r
Accept-Encoding: gzip, deflate, br\r
Accept-Language: en-US,en;q=0.9\r
Connection: keep-alive\r
Content-Length: 0\r
content-type: application/json\r
Host: localhost:8000\r
Origin: null\r
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36\r
\r
\r
"""
        mock_sock = Mock(socket)
        mock_sock.recv.return_value = test_request_post_json
        mock_sock.makefile.return_value = BytesIO(test_request_post_json)
        mock_serv = Mock(ShopHTTPServer)
        mock_serv.get_handler.return_value = (lambda hndl: None, {})
        hndl = RequestHandler(mock_sock, ("localhost", 8080), mock_serv)
        self.assertFalse(hasattr(hndl, "json_body"), "handler json_body parameter in DELETE request")

    def test_RequestHandler_success(self):
        test_request_post_json = b"""GET / HTTP/1.1\r
Accept: */*\r
Accept-Encoding: gzip, deflate, br\r
Accept-Language: en-US,en;q=0.9\r
Connection: keep-alive\r
Content-Length: 0\r
content-type: application/json\r
Host: localhost:8000\r
Origin: null\r
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36\r
\r
\r
"""
        with patch("socketserver._SocketWriter"):
            mock_sock = Mock(socket)
            mock_sock.recv.return_value = test_request_post_json
            mock_sock.makefile.return_value = BytesIO(test_request_post_json)
            mock_serv = Mock(ShopHTTPServer)
            mock_serv.get_handler.return_value = (lambda hndl: hndl.success({"test": "test"}), {})
            hndl = RequestHandler(mock_sock, ("localhost", 8080), mock_serv)
            mock_serv.get_handler.assert_called_once_with("GET", "/")
            hndl.wfile.write.assert_called()
            args = functools.reduce(lambda acc, it: acc + it[0][0], hndl.wfile.write.call_args_list, b"")
            startLine, msg = args.split(b"\r\n", 1)
            parser = BytesParser(policy=policy.HTTP)
            msg = parser.parsebytes(msg)
            self.assertEqual(b"HTTP/1.0 200 OK", startLine, "Response start line is not as expected")
            self.assertEqual("application/json", msg["Content-Type"], "Unexpected success response code")
            self.assertEqual({"error": False, "test": "test"},
                             json.loads(msg.get_content(content_manager=raw_data_manager),
                                        encoding="utf-8"),
                             "Incorrect body")

    def test_RequestHandler_error(self):
        test_request_post_json = b"""GET / HTTP/1.1\r
Accept: */*\r
Accept-Encoding: gzip, deflate, br\r
Accept-Language: en-US,en;q=0.9\r
Connection: keep-alive\r
Content-Length: 0\r
content-type: application/json\r
Host: localhost:8000\r
Origin: null\r
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36\r
\r
\r
"""
        with patch("socketserver._SocketWriter"):
            mock_sock = Mock(socket)
            mock_sock.recv.return_value = test_request_post_json
            mock_sock.makefile.return_value = BytesIO(test_request_post_json)
            mock_serv = Mock(ShopHTTPServer)
            mock_serv.get_handler.return_value = (lambda hndl: hndl.error(404, "", {"test": "test"}), {})
            hndl = RequestHandler(mock_sock, ("localhost", 8080), mock_serv)
            mock_serv.get_handler.assert_called_once_with("GET", "/")
            hndl.wfile.write.assert_called()
            args = functools.reduce(lambda acc, it: acc + it[0][0], hndl.wfile.write.call_args_list, b"")
            startLine, msg = args.split(b"\r\n", 1)
            parser = BytesParser(policy=policy.HTTP)
            msg = parser.parsebytes(msg)
            self.assertEqual(b"HTTP/1.0 404 Not Found", startLine, "Response start line is not as expected")
            self.assertEqual("application/json", msg["Content-Type"], "Unexpected success response code")
            self.assertEqual({"error": True, "test": "test"},
                             json.loads(msg.get_content(content_manager=raw_data_manager),
                                        encoding="utf-8"),
                             "Incorrect body")
