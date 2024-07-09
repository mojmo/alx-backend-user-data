#!/usr/bin/env python3

"""Basic Authentication"""

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
