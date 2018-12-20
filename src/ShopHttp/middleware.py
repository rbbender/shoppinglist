from json import load, dumps

def parse_json_body(hndl):
    if "Content-Type" in hndl.headers and hndl.headers["Content-Type"] == "application/json":
        if "Content-Length" in hndl.headers and int(hndl.headers["Content-Length"]):
            hndl.json_body = load(hndl.rfile)

