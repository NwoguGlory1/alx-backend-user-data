#!/usr/bin/env python3
""" Module of Session Authentication """

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ Session Authentication Class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ method that creates a Session ID for a user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id_generated = uuid.uuid4()
        """ Generates a new UUID using uuid4()"""
        session_id = str(session_id_generated)
        """ Convert the UUID to a string before using as key"""
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ method that returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        """
        .get() is used to access the value user_id for the key session_id
        """
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
