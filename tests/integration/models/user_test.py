from tests.base_test import BaseTest
from models.user import UserModel


class UserTest(BaseTest):

    def test_save_to_db(self):
        user = UserModel("Test", "Test Pass")

        with self.app_context():
            self.assertIsNone(user.find_by_username("Test"))
            self.assertIsNone(user.find_by_id(1))
            user.save_to_db()
            self.assertIsNotNone(user.find_by_username("Test"))
            self.assertIsNotNone(user.find_by_id(1))
