#!/usr/bin/env python3

"""
Authentication module for the authentication database.
"""

from typing import Union
import bcrypt
from db import DB
import uuid
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """
    Hash a password string using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: A salted hash of the input password.
    """
    # Encode the password string to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password


def _generate_uuid() -> str:
    """Generate a string representation of a new UUID.

    Returns:
        str: A string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User doesn't exist, so we can create a new one
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user's login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a session ID for the user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Retrieve a user based on a session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            User or None: The corresponding User object if found,
            otherwise None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for a user.

        Args:
            user_id (int): The ID of the user whose session should
            be destroyed.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for a user with the given email.

        Args:
            email (str): The email of the user requesting the reset
            password token.

        Returns:
            str: The generated reset password token.

        Raises:
            ValueError: If the user with the given email does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User with email {} does not exist".format(email))

        reset_token = str(uuid.uuid4())

        # Update the user's reset_token field in the database
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password using a reset token.

        Args:
            reset_token (str): The reset token used to identify the user.
            password (str): The new password to be set for the user.

        Returns:
            None

        Raises:
            ValueError: If the reset token does not correspond to any user.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        # Hash the new password
        hashed_password = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            )

        # Update the user's hashed_password field with the new hashed password
        self._db.update_user(user.id, hashed_password=hashed_password)

        # Set the user's reset_token field to None
        self._db.update_user(user.id, reset_token=None)

        return None
