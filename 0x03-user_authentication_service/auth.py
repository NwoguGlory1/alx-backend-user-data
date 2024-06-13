#!/usr/bin/env python3
"""Hash password """

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
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
