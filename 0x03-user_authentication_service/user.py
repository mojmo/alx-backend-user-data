#!/usr/bin/env python3

"""
This module defines the User model for interacting with the 'users'
table in the database. It uses SQLAlchemy ORM to map the User class
to the database table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):

    """
    Represents a user in the system.

    This class defines the structure of the 'users' table in the database.
    It includes fields for user identification, authentication,
    and password reset.

    Attributes:
        id (int): The primary key of the user.
        email (str): The user's email address. Must be unique and is required.
        hashed_password (str): The user's password, stored as a hash. Required.
        session_id (str): The user's current session ID. Optional.
        reset_token (str): A token for password reset functionality. Optional.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
