from tests.unit.unit_base_test import UnitBaseTest
from models.user import UserModel


class UserTest(UnitBaseTest):

    def test_instantiate_user(self):

        user = UserModel("Test", "Test Pass")

        self.assertEqual(user.username, "Test")
        self.assertEqual(user.password, "Test Pass")
