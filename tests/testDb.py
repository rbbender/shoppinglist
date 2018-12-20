from unittest import TestCase
from unittest.mock import patch, Mock
from bson.objectid import ObjectId

import db

class TestFindAll(TestCase):
    def test_empty_result(self):
        """Test empty result being returned as empty list"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.find.return_value = []
            MockConn.return_value = {'items': MockColl}
            self.assertEqual([], db.getAll('items', {'user': 'testUser'}), "Incorrect findall result")

    def test_exception(self):
        """Test exception handling"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.find.return_value = []
            MockColl.find.side_effect = Exception()
            MockConn.return_value = {'items': MockColl}
            self.assertRaises(Exception, db.getAll, 'items', {'user': 'testUser'})

    def test_one_record(self):
        """_id -> objId"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.find.return_value = [{"_id": ObjectId('12345678901234567890ABCD'), "userName": "testUN1",
                                           "displayName": "Test User Name 1"}]
            MockConn.return_value = {'items': MockColl}
            self.assertEqual([{"objId": '12345678901234567890abcd', "userName": "testUN1",
                               "displayName": "Test User Name 1"}], db.getAll('items', {'user': 'testUser'}),
                             "Incorrect findall result")

class TestFindOne(TestCase):
    def test_empty_result(self):
        """Test empty result being returned as empty list"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.find_one.return_value = None
            MockConn.return_value = {'items': MockColl}
            self.assertEqual(None, db.getOne('items', {'user': 'testUser'}), "Incorrect getOne result")

    def test_exception(self):
        """Test exception handling"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.find_one.return_value = []
            MockColl.find_one.side_effect = Exception()
            MockConn.return_value = {'items': MockColl}
            self.assertRaises(Exception, db.getOne, 'items', {'user': 'testUser'})

    def test_one_record(self):
        """_id -> objId"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.find_one.return_value = {"_id": ObjectId('12345678901234567890ABCD'), "userName": "testUN1",
                                              "displayName": "Test User Name 1"}
            MockConn.return_value = {'items': MockColl}
            self.assertEqual({"objId": '12345678901234567890abcd', "userName": "testUN1",
                              "displayName": "Test User Name 1"}, db.getOne('items', {'user': 'testUser'}),
                              "Incorrect getOne result")

class TestDeleteOne(TestCase):
    def test_empty_result(self):
        """Test empty result being returned as empty list"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.find_one_and_delete.return_value = None
            MockConn.return_value = {'items': MockColl}
            self.assertEqual(None, db.deleteOne('items', {'user': 'testUser'}), "Incorrect deleteOne result")

    def test_exception(self):
        """Test exception handling"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.find_one_and_delete.return_value = []
            MockColl.find_one_and_delete.side_effect = Exception()
            MockConn.return_value = {'items': MockColl}
            self.assertRaises(Exception, db.deleteOne, 'items', {'user': 'testUser'})

    def test_one_record(self):
        """_id -> objId"""
        with patch('db.queries.connection') as MockConn:
            delete_result = {"_id": ObjectId('12345678901234567890ABCD'),
                                        "userName": "testUN1",
                                        "displayName": "Test User Name 1"}
            MockColl = Mock()
            MockColl.find_one_and_delete.return_value = delete_result
            MockConn.return_value = {'items': MockColl}
            self.assertEqual({"objId": '12345678901234567890abcd', "userName": "testUN1",
                              "displayName": "Test User Name 1"}, db.deleteOne('items', {'user': 'testUser'}),
                              "Incorrect deleteOne result")

class TestAddOne(TestCase):
    def test_empty_result(self):
        """Test empty result being returned as empty list"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.insert_one.return_value = None
            MockConn.return_value = {'items': MockColl}
            self.assertEqual(None, db.addOne('items', {'user': 'testUser'}), "Incorrect addOne result")

    def test_exception(self):
        """Test exception handling"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.insert_one.return_value = []
            MockColl.insert_one.side_effect = Exception()
            MockConn.return_value = {'items': MockColl}
            self.assertRaises(Exception, db.addOne, 'items', {'user': 'testUser'})

    def test_one_record(self):
        """_id -> objId"""
        with patch('db.queries.connection') as MockConn:
            insert_result = Mock()
            insert_result.inserted_id = ObjectId('12345678901234567890ABCD')
            MockColl = Mock()
            MockColl.insert_one.return_value = insert_result
            MockConn.return_value = {'items': MockColl}
            self.assertEqual({"objId": '12345678901234567890abcd'}, db.addOne('items', {'user': 'testUser'}),
                              "Incorrect addOne result")

class TestUpdateOne(TestCase):
    def test_empty_result(self):
        """Test empty result being returned as empty list"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.find_one_and_update.return_value = None
            MockConn.return_value = {'items': MockColl}
            self.assertEqual(None, db.updateOne('items', {'user': 'testUser'}, {"update": "update1"}),
                             "Incorrect addOne result")

    def test_exception(self):
        """Test exception handling"""
        with patch('db.queries.connection') as MockConn:
            MockColl = Mock()
            MockColl.find_one_and_update.return_value = []
            MockColl.find_one_and_update.side_effect = Exception()
            MockConn.return_value = {'items': MockColl}
            self.assertRaises(Exception, db.updateOne, 'items', {'user': 'testUser'}, {"update": "update1"})

    def test_one_record(self):
        """_id -> objId"""
        with patch('db.queries.connection') as MockConn:
            update_result = Mock()
            update_result = {"_id": ObjectId('12345678901234567890ABCD'),
                             "userName": "testUN1",
                             "displayName": "Test User Name 1"}
            MockColl = Mock()
            MockColl.find_one_and_update.return_value = update_result
            MockConn.return_value = {'items': MockColl}
            self.assertEqual({"objId": '12345678901234567890abcd', "userName": "testUN1",
                              "displayName": "Test User Name 1"}, db.updateOne('items', {'user': 'testUser'},
                                                                               {"update": "update1"}),
                              "Incorrect addOne result")
