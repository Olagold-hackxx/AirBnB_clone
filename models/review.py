#!/usr/bin/python3

"""
Module contain class `Review` that
defines all reviews in Airbnb project
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Class that handles reviews"""

    place_id = ""
    user_id = ""
    text = ""
