#!/usr/bin/env python3

"""Manage session authentication with database"""

from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class to manage session authentication with database"""

    def create_session(self, user_id=None):
        """ Create a session and store it in the database """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_info = {
            'user_id': user_id,
            'session_id': session_id
        }
        user_session = UserSession(**session_info)
        user_session.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve a user ID based on a session ID """
        if not session_id:
            return None

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})

        if not sessions:
            return None

        session = sessions[0]
        session_time = session.created_at + \
            timedelta(seconds=self.session_duration)

        if datetime.now() > session_time:
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """ Delete a session from the database """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        session = sessions[0]
        try:
            session.remove()
            UserSession.save_to_file()
            return True
        except Exception:
            return False
