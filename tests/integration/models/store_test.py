from models.item import ItemModel
from tests.base_test import BaseTest
from models.store import StoreModel


class StoreTest(BaseTest):

    def test_create_store_empty(self):
        store = StoreModel("Test")

        self.assertListEqual(store.items.all(), [])

    def test_json(self):
        store = StoreModel("Test")
        expected_json = {'name': "Test", 'items': []}

        self.assertDictEqual(store.json(), expected_json)

    def test_crud(self):

        with self.app_context():

            store = StoreModel("Test")
            self.assertIsNone(store.find_by_name("Test"))

            store.save_to_db()
            self.assertIsNotNone(store.find_by_name("Test"))

            store.delete_from_db()
            self.assertIsNone(store.find_by_name("Test"))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("Test")
            item = ItemModel("Test Item", 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, "Test Item")
            self.assertEqual(store.items.first().price, 19.99)
            self.assertEqual(store.items.first().store_id, 1)
