#!/usr/bin/env python3

"""Hashes a password using bcrypt."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates a password against a hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
