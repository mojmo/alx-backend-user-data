#!/usr/bin/env python3

"""
This module provides an `Auth` class for basic authentication functionalities
in a Flask application.
"""

from typing import List, TypeVar
from flask import request


class Auth():
    """
    This class serves as a basic framework for authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required for a given request path."""

        return False

    def authorization_header(self, request=None) -> str:
        """
        Attempts to retrieve the authorization header from the Flask
        request object (if provided).
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Attempts to extract the current user information from the
        authorization header (if available).
        """
        return None
