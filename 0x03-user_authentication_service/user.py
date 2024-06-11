#!/usr/bin/env python3
""" """
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
""" for creating a declarative base class."""

Base = declarative_base()
""" declarative base class """

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email Column(nullable=False, String) ,
    hashed_password Column(nullable=False, String),
    session_id Column(nullable=True String),
    reset_token Column(nullable=True, String),
