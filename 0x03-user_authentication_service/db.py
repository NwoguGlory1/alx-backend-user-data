#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base
from user import User

class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        method to save the user to the database.
        Has two required string args: email and hashed_password
        returns a User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        # Create a new User object with args
        session = self._session
        session.add(user)
        # use the DB class's _session property to interact
        # with the database.
        # Add the User object to the database session
        # with _session.add().
        session.commit()
        # Comit changes with  _session.commit()
        return user