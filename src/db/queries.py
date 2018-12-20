from . import connection
from bson.objectid import ObjectId, InvalidId
from pymongo import ReturnDocument

def _postprocess(rec):
    if rec and isinstance(rec, dict) and "_id" in rec and isinstance(rec["_id"], ObjectId):
        rec["objId"] = str(rec["_id"])
        del rec["_id"]
    return rec

def _preprocess_criteria(criteria):
    if "_id" in criteria and isinstance(criteria["_id"], str):
        criteria["_id"] = ObjectId(criteria["_id"])
    return criteria

def getAll(collName, criteria={}, projection=None):
    conn = connection()
    try:
        return [_postprocess(rec) for rec in conn[collName].find(filter=criteria, projection=projection)]
    except:
        raise

def getOne(collName, criteria={}, projection=None):
    conn=connection()
    try:
        _preprocess_criteria(criteria)
    except InvalidId:
        return None
    try:
        return _postprocess(conn[collName].find_one(filter=criteria, projection=projection))
    except:
        raise

def addOne(collName, doc):
    conn=connection()
    try:
        result = conn[collName].insert_one(doc)
        if result:
            return _postprocess({"_id": result.inserted_id})
        return None

    except:
        raise

def updateOne(collName, criteria={}, update={}):
    conn=connection()
    try:
        _preprocess_criteria(criteria)
    except InvalidId:
        return None
    try:
        result = conn[collName].find_one_and_update(filter=criteria, update={"$set": update},
                                                    return_document=ReturnDocument.AFTER)
        return _postprocess(result)
    except:
        raise

def deleteOne(collName, criteria={}):
    conn=connection()
    try:
        _preprocess_criteria(criteria)
    except InvalidId:
        return None
    try:
        result = conn[collName].find_one_and_delete(filter=criteria)
        return _postprocess(result)
    except:
        raise
