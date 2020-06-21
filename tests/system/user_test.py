from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):

    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/register", data={"username": "Test", "password": "1234"})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username("Test"))
                self.assertDictEqual({"message": "User created."}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={"username": "Test", "password": "1234"})
                auth_response = client.post("/auth", data=json.dumps(
                    {"username": "Test", "password": "1234"}), headers={"Content-Type": "application/json"}
                )

                self.assertIn("access_token", json.loads(auth_response.data).keys())

    def test_user_duplicates(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={"username": "Test", "password": "1234"})
                response = client.post("/register", data={"username": "Test", "password": "1234"})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data), {"message": "User already exist."})
