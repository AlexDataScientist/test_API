from models.item import ItemModel
from tests.base_test import BaseTest
from models.store import StoreModel
import json


class StoreTest(BaseTest):

    def test_create_store(self):

        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(response.data), {"name": "test", "items": []})

    def test_create_duplicates_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': "A store with name 'test' already exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.delete('/store/test')

                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'message': 'Store deleted'})

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/test')
                response = client.get('store/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {"name": "test", "items": []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), {'message': 'Store not found'})

    def test_find_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test").save_to_db()
                ItemModel("Test Item", 19.99, 1).save_to_db()

                response = client.get('/store/Test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {"name": "Test",
                                      "items": [
                                          {"name": "Test Item", "price": 19.99}
                                      ]})

    def find_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'stores': [
                                         {"name": "test", "items": []}
                                     ]})

    def find_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                ItemModel("Test item", 18.99, 1).save_to_db()
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'stores': [
                                         {"name": "test",
                                          "items": [{"name": "Test Item", "price": 18.99}]}
                                     ]})
