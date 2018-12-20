from db import getOne, addOne, getAll, deleteOne, updateOne
from ShopHttp import RequestHandler

def _cleanUpItemDictPreUpdate(dct):
    for k in ["itemId", "_id"]:
        if k in dct:
            del dct[k]

def _substituteItemId(dct):
    if "_id" in dct:
        dct["itemId"] = dct["_id"]
        del dct["_id"]

def _verifyItemToAdd(dct):
    for k in ["name"]:
        if k not in dct:
            return False
    return True

def getAllItems(handler):
    if not isinstance(handler, RequestHandler):
        raise Exception("Incorrect HTTP handler given")
    try:
        items = getAll("items")
        handler.success({"items": items})
    except Exception as e:
        handler.log_error()
        handler.error(500, f"Error in getAllItems: {e}", {"message": "Error getting shopping list"})

def getItem(handler):
    if not isinstance(handler, RequestHandler):
        raise Exception("Incorrect HTTP handler given")
    try:
        itemId = handler.params["itemId"]
        item = getOne("items", {"_id": itemId})
        if item is None:
            handler.error(404, f"Item {itemId} not found", {"message": "Shopping item not found"})
        else:
            _substituteItemId(item)
            handler.success({"item": item})
    except Exception as e:
        handler.error(500, f"Error in getItem: {e}", {"message": "Error getting shopping item"})


def addItem(handler):
    if not isinstance(handler, RequestHandler):
        raise Exception("Incorrect HTTP handler given")
    try:
        objSpec = dict(handler.json_body.items())
        _cleanUpItemDictPreUpdate(objSpec)
        if not _verifyItemToAdd(objSpec):
            handler.error(400, f"Item verification failed: {objSpec}", {"message": "Incorrect item to add"})
        else:
            addedItem = addOne("items", objSpec)
            if addedItem is not None:
                _substituteItemId(addedItem)
                handler.success({"item": addedItem})
            else:
                raise Exception("addOne returned None")
    except Exception as e:
        handler.error(500, f"Error in addOne: {e}", {"message": "Unable to add shopping item"})



def updateItem(handler):
    if not isinstance(handler, RequestHandler):
        raise Exception("Incorrect HTTP handler given")
    try:
        itemId = getattr(handler, "params", {}).get("itemId", None)
        if itemId:
            updateDict = dict(handler.json_body)
            _cleanUpItemDictPreUpdate(updateDict)
            updatedItem = updateOne("items", {"_id": itemId}, updateDict)
        if itemId is None: # no itemId in params
            handler.error(404, f"No ItemId in path", {"message": "Incorrect item to update"})
            return
        elif updatedItem is None: # not found
            handler.error(404, f"ItemId {itemId} not found", {"message": "Incorrect item to update"})
            return
        else:
            _substituteItemId(updatedItem)
            handler.success({"item": updatedItem})
            return
    except Exception as e:
        handler.error(500, f"Error in updateOne: {e}", {"message": "Unable to update shopping item"})


def deleteItem(handler):
    if not isinstance(handler, RequestHandler):
        raise Exception("Incorrect HTTP handler given")
    try:
        itemId = getattr(handler, "params", {}).get("itemId", None)
        if itemId:
            deletedItem = deleteOne("items", {"_id": itemId})
        if itemId is None or deletedItem is None:
            handler.error(404, f"Item {itemId} not found", {"message": "Incorrect item to delete"})
        else:
            handler.success({"message": "Item deleted"})
    except Exception as e:
        handler.error(500, f"Error in deleteOne: {e}", {"message": "Unable to delete shopping item"})

