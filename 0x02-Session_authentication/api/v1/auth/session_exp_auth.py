#!/usr/bin/env python3

"""Session authentication with expiration"""

from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication with expiration"""
    def __init__(self):
        """
        Initialize the session duration from environment variables
        """

        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session with an expiration time
        """

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return user_id based on the session ID and its expiration
        """
        if not session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_at' not in session_dict:
            return None

        creation_time = session_dict['created_at']
        expired_time = creation_time + timedelta(seconds=self.session_duration)

        if expired_time < datetime.now():
            return None

        return session_dict.get('user_id')
