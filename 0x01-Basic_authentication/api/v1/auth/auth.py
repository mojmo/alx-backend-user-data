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
        """
        Checks if authentication is required for a given request path.

        Args:
            path: The request path (string).
            excluded_paths: A list of paths (strings) exempt from
            authentication. All elements in the list are assumed
            to end with a trailing slash (/).

        Returns:
            True if authentication is required, False otherwise.
        """

        if path is None or not excluded_paths:
            return True

        # Standardize path by removing trailing slash (if present)
        path = path.rstrip('/')

        # Check if path is a perfect match or a prefix of any excluded path
        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/')
            if path == excluded_path or path.startswith(excluded_path + '/'):
                return False

        # No match found, authentication required
        return True

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
