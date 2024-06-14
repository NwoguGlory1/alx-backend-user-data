#!/usr/bin/env python3
"""Hash password """

from db import DB
from user import User
from typing import Union
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid
# Import the necessary libraries, exception


def _hash_password(password: str) -> bytes:
    """
    method to use bcrypt.hashpw to
    generate a salted hash of the input password.
    """
    password_in_bytes = password.encode("UTF-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_in_bytes, salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate a new UUID."""
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user in the database """
        try:
            # Try to find a user with the given email
            existing_user = self._db.find_user_by(email=email)
        except NoResultFound:
            # If no existing user, hash the password& add a new user
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)

            # Return the new user
            return new_user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ Logs in user """
        try:
            # Try to find a user with the given email
            located_user = self._db.find_user_by(email=email)

            # Check if a user was found
            if located_user is not None:
                # Retrieve the hashed password from the user object
                stored_hashed_password = located_user.hashed_password
                # Check if provided password matches stored hashed pa..
                if bcrypt.checkpw(password.encode(), stored_hashed_password):
                    return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """ Returns session ID for a user """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()

        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """It takes a single session_id string argument
        Returns a string or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user's session ID to None"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)

        return None
