import argparse
from ShopHttp import ShopHTTPServer
from db import connect
from Routes import getAllItems, getItem, updateItem, deleteItem, addItem

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Simple REST API server for shopping list")
    db_group = arg_parser.add_argument_group("DB connection")
    db_group.add_argument("db_url", default="mongodb://localhost:27017", help="MongoDB URL")
    db_group.add_argument("db_name", default="test", help="DB name")
    db_group.add_argument("db_username", default="tester", help="Username to connect to DB")
    db_group.add_argument("db_pass", default="tester42", help="Password to connect to DB")
    arg_parser.add_argument("host", default="", help="Interface to serve on")
    arg_parser.add_argument("port", default=8989, type=int, help="Port to serve on")
    parsed = arg_parser.parse_args()

    try:
        connect(parsed.db_url, parsed.db_name, parsed.db_username, parsed.db_pass)
    except:
        print("Error: unable to connect to DB")
        exit(1)

    try:
        serv = ShopHTTPServer((parsed.host, parsed.port))
        serv.add_handler("GET", "/", getAllItems)
        serv.add_handler("GET", "/{itemId}", getItem)
        serv.add_handler("PATCH", "/{itemId}", updateItem)
        serv.add_handler("POST", "/", addItem)
        serv.add_handler("DELETE", "/{itemId}", deleteItem)
        serv.serve_forever()
    except:
        print("Error listening on port")
        raise

