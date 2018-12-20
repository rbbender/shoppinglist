from http.server import BaseHTTPRequestHandler
from json import loads, dumps

class RequestHandler(BaseHTTPRequestHandler):
    def process_request(self):
        self._parse_json()
        handler, params = self.server.get_handler(self.command, self.path)
        self.params = params
        if handler is None:
            return self.error(400, "Handler not found", {"message": "Unknown path"})
        try:
            return handler(self)
        except Exception as e:
            self.error(500, f"Exception: {e}", {"message": "internal error"})

    def _send_content_with_length(self, body):
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _parse_json(self):
        if "Content-Type" in self.headers and self.headers["Content-Type"] == "application/json":
            length = int(self.headers.get("content-length", "0"))
            if length > 0:
                body = self.rfile.read(length)
                self.json_body = loads(body, encoding="utf-8")

    def _send_json(self, dct):
        try:
            str_body = dumps(dct)
            self.send_header("content-type", "application/json")
            return self._send_content_with_length(str_body)
        except Exception as e:
            self.error(500, f"Error sending json: {dct}, exception: {e}", {"message": "Error sending response"})
            return

    def error(self, code, log_message, body):
        if "error" not in body:
            body["error"] = True
        self.log_error(log_message)
        self.send_response(code)
        self._send_json(body)

    def success(self, body):
        if "error" not in body:
            body["error"] = False
        self.send_response(200)
        self._send_json(body)

    def do_POST(self):
        self.process_request()

    def do_GET(self):
        self.process_request()

    def do_PATCH(self):
        self.process_request()

    def do_DELETE(self):
        self.process_request()