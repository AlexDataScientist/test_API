from tests.base_test import BaseTest
from models.user import UserModel
from models.store import StoreModel
from models.item import ItemModel
import json


class ItemTest(BaseTest):

    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel("Test User", "1234").save_to_db()
                auth_response = client.post('/auth',
                                            data=json.dumps({"username": "Test User",
                                                             "password": "1234"}),
                                            headers={"Content-Type": "application/json"})

                auth_request = json.loads(auth_response.data)["access_token"]
                self.access_token = "JWT " + auth_request

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')

                self.assertEqual(response.status_code, 400)

    def test_get_item_not_found(self):

        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test', headers={"Authorization": self.access_token})

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), {'message': 'Item not found'})

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store").save_to_db()
                ItemModel("test", 20, 1).save_to_db()
                response = client.get('/item/test', headers={"Authorization": self.access_token})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'name': "test", 'price': 20})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store").save_to_db()
                ItemModel("test", 19, 1).save_to_db()

                self.assertIsNotNone(ItemModel.find_by_name('test'))

                response = client.delete('/item/test', headers={"Authorization": self.access_token})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'message': 'Item deleted'})

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store").save_to_db()
                response = client.post('/item/test',
                                       data={"price": 19.99, "store_id": 1},
                                       headers={"Authorization": self.access_token})

                self.assertIsNotNone(ItemModel.find_by_name('test'))
                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(json.loads(response.data),
                                     {'name': 'test', 'price': 19.99})

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Store Model").save_to_db()
                ItemModel("test", 10.00, 1).save_to_db()

                response = client.post("/item/test", data={"price": 89.00, "store_id": 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': "An item with name 'test' already exists."})

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store").save_to_db()

                response = client.put("/item/test", data={"price": 19.99, "store_id": 1})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'name': 'test', 'price': 19.99})

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()

                response = client.put("/item/test", data={"price": 99.99, "store_id": 1})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response. data), {'name': 'test', 'price': 99.99})

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Store Test").save_to_db()
                ItemModel("test 1", 19.99, 1).save_to_db()
                ItemModel("test 2", 15.99, 1).save_to_db()

                response = client.get("/items")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'items': [{'name': 'test 1', 'price': 19.99},
                                                {'name': 'test 2', 'price': 15.99}]})
