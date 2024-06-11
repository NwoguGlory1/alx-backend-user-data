#!/usr/bin/env python3
""" Expiration script """
import os
import datetime
from api.v1.auth.session_auth import SessionAuth

class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class """
    
    def __init__(self):
        """
        method that initializes session duration from
        the SESSION_DURATION environment variable.
        """
        self.session_duration = int(os.environ.get('SESSION_DURATION', 0))
        if not self.session_duration:
            self.session_duration = 0
 
    def create_session(self, user_id=None):
        """ Creates a new session, stores UserID & creation time """
        session_id = super().create_session()
        if session_id is None:
            return None 
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the user ID for a given session ID"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if 'created_at' not in session_dict:
            expiration_date = session_dict['created_at'] + datetime.timedelta(seconds=self.session_duration)
            """ adds session duration to 'created_at' datetime """
        if expiration_date < datetime.datetime.now():
            return None
        return session_dict.get('user_id')