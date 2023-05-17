#!/usr/bin/python3

"""
Module contain class `User` that
defines all users details
"""
from models.base_model import BaseModel


class User(BaseModel):
    """Class that handles user details"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
