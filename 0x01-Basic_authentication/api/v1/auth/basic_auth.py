#!/usr/bin/env python3

"""Basic Authentication"""

from base64 import b64decode
from api.v1.auth.auth import Auth


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

        user_credentials = decoded_base64_authorization_header.split(':')

        return user_credentials[0], user_credentials[1]
