#!/usr/bin/env python3

"""Manage user sessions"""

from models.base import Base


class UserSession(Base):
    """UserSession class to manage user sessions"""
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize UserSession instance """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
