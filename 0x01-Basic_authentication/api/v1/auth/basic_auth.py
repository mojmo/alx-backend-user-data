#!/usr/bin/env python3

"""Basic Authentication"""

from base64 import b64decode
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication Class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract the base64 encoded string from the authorization header"""
        if (
             authorization_header is None or
             not isinstance(authorization_header, str) or
             not authorization_header.startswith("Basic ")):
            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
             self, base64_authorization_header: str) -> str:
        """Decode the base64 encoded string from the authorization header"""
        if (base64_authorization_header is None or
           not isinstance(base64_authorization_header, str)):
            return None

        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None

        return decoded

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract the user credentials from the decoded base64 encoded string
        """
        if (decoded_base64_authorization_header is None or
           not isinstance(decoded_base64_authorization_header, str) or
           not decoded_base64_authorization_header.count(':')):
            return None, None

        user_credentials = decoded_base64_authorization_header.split(':', 1)

        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Create a user object from the user credentials
        """

        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request based on the
        authorization header
        """

        if request is None:
            return None

        authorization_header = request.headers.get('Authorization')
        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)

        if base64_authorization_header is None:
            return None

        decoded_credentials = self.decode_base64_authorization_header(
            base64_authorization_header)
        if decoded_credentials is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decoded_credentials)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
