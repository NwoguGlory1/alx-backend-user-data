#!/usr/bin/env python3
"""Hash password """

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    method to use bcrypt.hashpw to
    generate a salted hash of the input password.
    """
    password_in_bytes = password.encode("UTF-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_in_bytes, salt)
    return hashed_password
