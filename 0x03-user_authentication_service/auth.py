#!/usr/bin/env python3

"""
Hash a password string using bcrypt.
"""

import bcrypt


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
