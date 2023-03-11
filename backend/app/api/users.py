import json
from typing import final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from backend.app.database import User
from .auxiliary import post_request, get_request, post_failure, HTTPErrorCode
from backend.app.database.user import Role


class Users(Resource):
    route: final(str) = '/users'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:
        return Response(json.dumps([user.to_json() for user in User.get_all_users()]), 200)

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def post() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str, location='json', required=True)
        parser.add_argument('name', type=str, location='json', required=True)
        parser.add_argument('comment', type=str, location='json', required=True)
        parser.add_argument('password', type=str, location='json', required=True)
        parser.add_argument('role', type=str, location='json', required=True)
        arguments = parser.parse_args()

        if User.get_by_login(arguments['login']) is not None:
            return post_failure(HTTPErrorCode.CONFLICTING_ARGUMENTS, 400)

        role = arguments['role']
        if role is not None:
            role = Role[role]

        new_user = User(arguments['login'], arguments['name'], arguments['comment'], arguments['password'], role)
        new_user.save_to_db()
        return Response(str(new_user.id), 200)

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def patch() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json', required=True)
        parser.add_argument('login', type=str, location='json', required=False, default=None)
        parser.add_argument('name', type=str, location='json', required=False, default=None)
        parser.add_argument('comment', type=str, location='json', required=False, default=None)
        parser.add_argument('password', type=str, location='json', required=False, default=None)
        parser.add_argument('role', type=str, location='json', required=False, default=None)
        arguments = parser.parse_args()

        user = User.get_by_id(arguments['id'])
        if user is None:
            return post_failure(HTTPErrorCode.WRONG_ID, 404)

        new_password = arguments['password']
        if new_password is not None and user.check_password(new_password):
            new_password = None
        new_role = arguments['role']
        if new_role is not None:
            new_role = Role[new_role]
        user.update(arguments['login'], arguments['name'], arguments['comment'], new_password, new_role)
        return Response(str(user.id), 200)
