from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="username is a required argument."
    )

    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="password is a required argument."
    )

    def post(self):

        data = self.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "User already exist."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created."}, 201
