#!/usr/bin/python3

"""
Module contain class `City` that
defines all cities in Airbnb project
"""
from models.base_model import BaseModel


class City(BaseModel):
    """Class that handles cities"""

    name = ""
    state_id = ""
