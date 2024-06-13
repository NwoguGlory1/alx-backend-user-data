#!/usr/bin/env python3
"""Hash password """

import bcrypt

def _hash_password(password: str) -> bytes:
    """ """
    password_in_bytes = password.encode("UTF-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    bcrypt.hashpw(password, salt)
