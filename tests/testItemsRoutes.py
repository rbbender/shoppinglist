import unittest
from unittest.mock import Mock, patch
from ShopHttp import RequestHandler

from Routes import getAllItems, getItem, addItem, deleteItem, updateItem

def return_emulated_mock():
    res = Mock(RequestHandler)
    res.send_json = Mock()
    return res

class TestRouteGetItems(unittest.TestCase):
    def test_incorrect_call(self):
        handler = None
        self.assertRaises(Exception, getAllItems, handler)

    def test_empty_return(self):
        with patch('Routes.itemsRoutes.getAll') as mockGetAll:
            mockGetAll.return_value = []
            mockHndl = return_emulated_mock()
            getAllItems(mockHndl)
            mockGetAll.assert_called_once_with("items")
            mockHndl.success.assert_called_once_with({"items": []})

    def test_exception_during_db_op(self):
        with patch("Routes.itemsRoutes.getAll") as mockGetAll:
            mockGetAll.side_effect = Exception("Failed DB operation")
            mockHndl = return_emulated_mock()
            getAllItems(mockHndl)
            mockGetAll.assert_called_once_with("items")
            mockHndl.error.assert_called_once_with(500, "Error in getAllItems: Failed DB operation",
                                                   {"message": "Error getting shopping list"})

    def test_normal_return(self):
        with patch('Routes.itemsRoutes.getAll') as mockGetAll:
            mockGetAll.return_value = [{"objId": "1", "name": "name 1"},
                                       {"objId": "ffffffdfdfdfdfd", "name": "name 2",
                                        "quantity": 45},
                                       {"objId": "aaaaacccccccc", "name": "name 3", "quantity": 34, "done": True}]

            mockHndl = return_emulated_mock()
            getAllItems(mockHndl)
            mockGetAll.assert_called_once_with("items")
            mockHndl.success.assert_called_once_with({"items": [{"objId": "1", "name": "name 1"},
                                       {"objId": "ffffffdfdfdfdfd", "name": "name 2",
                                        "quantity": 45},
                                       {"objId": "aaaaacccccccc", "name": "name 3", "quantity": 34, "done": True}]})


class TestRouteGetItem(unittest.TestCase):
    def test_incorrect(self):
        hndl = None
        self.assertRaises(Exception, getItem, hndl, {"taskId": "123"})

    def test_not_found(self):
        with patch("Routes.itemsRoutes.getOne") as mockGetOne:
            mockGetOne.return_value = None
            mockHndl = return_emulated_mock()
            mockHndl.params = {"itemId": "1234"}
            getItem(mockHndl)
            mockGetOne.assert_called_once_with("items", {"_id": "1234"})
            mockHndl.error.assert_called_once_with(404, "Item 1234 not found", {"message": "Shopping item not found"})

    def test_found(self):
        with patch("Routes.itemsRoutes.getOne") as mockGetOne:
            mockGetOne.return_value = {"_id": "1234", "name": "name 1", "quantity": 34, "done": True}
            mockHndl = return_emulated_mock()
            mockHndl.params = {"itemId": "1234"}
            getItem(mockHndl)
            mockGetOne.assert_called_once_with("items", {"_id": "1234"})
            mockHndl.success.assert_called_once_with({"item": {"itemId": "1234",
                                                               "name": "name 1",
                                                               "quantity": 34,
                                                               "done": True}
                                                        })

    def test_db_exception(self):
        with patch("Routes.itemsRoutes.getOne") as mockGetOne:
            mockGetOne.return_value = {"objId": "1234", "name": "name 1", "quantity": 34, "done": True}
            mockGetOne.side_effect = Exception("DB exception")
            mockHndl = return_emulated_mock()
            mockHndl.params = {"itemId": "1234"}
            getItem(mockHndl)
            mockGetOne.assert_called_once_with("items", {"_id": "1234"})
            mockHndl.error.assert_called_once_with(500, "Error in getItem: DB exception",
                                                   {"message": "Error getting shopping item"})


class TestRouteAddItem(unittest.TestCase):
    def test_incorrect_call(self):
        hndl = None
        self.assertRaises(Exception, addItem, hndl)

    def test_incorrect_item(self):
        with patch("Routes.itemsRoutes.addOne") as mockAddOne:
            mockHndl = return_emulated_mock()
            mockHndl.json_body = {}
            addItem(mockHndl)
            mockAddOne.assert_not_called()
            mockHndl.error.assert_called_once_with(400, "Item verification failed: {}", {"message": "Incorrect item to add"})

    def test_db_exception(self):
        with patch("Routes.itemsRoutes.addOne") as mockAddOne:
            mockHndl = return_emulated_mock()
            mockHndl.json_body = {"name": "name 1"}
            mockAddOne.side_effect = Exception("DB Exception")
            addItem(mockHndl)
            mockAddOne.assert_called_once_with("items", {"name": "name 1"})
            mockHndl.error.assert_called_once_with(500, "Error in addOne: DB Exception",
                                                   {"message": "Unable to add shopping item"})

    def test_success_add(self):
        with patch("Routes.itemsRoutes.addOne") as mockAddOne:
            mockHndl = return_emulated_mock()
            mockHndl.json_body = {"name": "name 2"}
            mockAddOne.return_value = {"_id": "1234", "name": "name 2"}
            addItem(mockHndl)
            mockAddOne.assert_called_once_with("items", {"name": "name 2"})
            mockHndl.success.assert_called_once_with({"item": {"itemId": "1234", "name": "name 2"}})


class TestRouteDeleteItem(unittest.TestCase):
    def test_incorrect_call(self):
        hndl = None
        self.assertRaises(Exception, deleteItem, hndl)

    def test_incorrect_item(self):
        with patch("Routes.itemsRoutes.deleteOne") as mockDeleteOne:
            mockHndl = return_emulated_mock()
            mockHndl.params = {}
            deleteItem(mockHndl)
            mockDeleteOne.assert_not_called()
            mockHndl.error.assert_called_once_with(404, "Item None not found", {"message": "Incorrect item to delete"})

    def test_db_exception(self):
        with patch("Routes.itemsRoutes.deleteOne") as mockDeleteOne:
            mockHndl = return_emulated_mock()
            mockHndl.params = {"itemId": "1234"}
            mockDeleteOne.side_effect = Exception("DB Exception")
            deleteItem(mockHndl)
            mockDeleteOne.assert_called_once_with("items", {"_id": "1234"})
            mockHndl.error.assert_called_once_with(500, "Error in deleteOne: DB Exception",
                                                   {"message": "Unable to delete shopping item"})

    def test_success_delete(self):
        with patch("Routes.itemsRoutes.deleteOne") as mockDeleteOne:
            mockHndl = return_emulated_mock()
            mockHndl.params = {"itemId": "1234"}
            mockDeleteOne.return_value = {"itemId": "1234", "name": "name 2"}
            deleteItem(mockHndl)
            mockDeleteOne.assert_called_once_with("items", {"_id": "1234"})
            mockHndl.success.assert_called_once_with({"message": "Item deleted"})

class TestRouteUpdateItem(unittest.TestCase):
    def test_incorrect_call(self):
        hndl = None
        self.assertRaises(Exception, updateItem, hndl)

    def test_incorrect_item_no_id(self):
        with patch("Routes.itemsRoutes.updateOne") as mockUpdateOne:
            mockHndl = return_emulated_mock()
            mockHndl.json_body = {"name": "name-change"}
            mockHndl.params = {}
            updateItem(mockHndl)
            mockUpdateOne.assert_not_called()
            mockHndl.error.assert_called_once_with(404, "No ItemId in path", {"message": "Incorrect item to update"})

    def test_incorrect_item_no_item_found(self):
        with patch("Routes.itemsRoutes.updateOne") as mockUpdateOne:
            mockHndl = return_emulated_mock()
            mockHndl.json_body = {"name": "name-change"}
            mockHndl.params = {"itemId": "1234"}
            mockUpdateOne.return_value = None
            updateItem(mockHndl)
            mockUpdateOne.assert_called_once_with("items", {"_id": "1234"}, {"name": "name-change"})
            mockHndl.error.assert_called_once_with(404, "ItemId 1234 not found",
                                                   {"message": "Incorrect item to update"})


    def test_db_exception(self):
        with patch("Routes.itemsRoutes.updateOne") as mockUpdateOne:
            mockHndl = return_emulated_mock()
            mockHndl.json_body = {"name": "name-change"}
            mockHndl.params = {"itemId": "1234"}
            mockUpdateOne.side_effect = Exception("Failed DB operation")
            updateItem(mockHndl)
            mockUpdateOne.assert_called_once_with("items", {"_id": "1234"}, {"name": "name-change"})
            mockHndl.error.assert_called_once_with(500, "Error in updateOne: Failed DB operation",
                                                   {"message": "Unable to update shopping item"})

    def test_success_add(self):
        with patch("Routes.itemsRoutes.updateOne") as mockUpdateOne:
            mockHndl = return_emulated_mock()
            mockHndl.json_body = {"name": "name-change"}
            mockHndl.params = {"itemId": "1234"}
            mockUpdateOne.return_value = {"itemId": "1234", "name": "name-change"}
            updateItem(mockHndl)
            mockUpdateOne.assert_called_once_with("items", {"_id": "1234"}, {"name": "name-change"})
            mockHndl.success.assert_called_once_with({"item": {"itemId": "1234", "name": "name-change"}})


if __name__ == '__main__':
    unittest.main()
