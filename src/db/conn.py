from pymongo import MongoClient
_dbconn = None

def connect(url, dbName, user, password, timeoutSec=20):
    connStr = f"{url}/{dbName}"
    global _dbconn
    _dbconn = MongoClient(connStr, username=user, password=password, serverSelectionTimeoutMS=timeoutSec*1000,
                         connect=False)
    try:
        _dbconn.admin.command('ismaster')
        _dbconn = _dbconn[dbName]
    except Exception as e:
        print(f"ERROR: {e!r}")
        raise

def connection():
    return _dbconn