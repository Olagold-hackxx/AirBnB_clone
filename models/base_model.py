#!/usr/bin/python3

"""
Module contain class `Basemodel` that
defines all common attributes/methods for other classess
"""
import uuid
from datetime import datetime


class BaseModel:
    """ Class that defines all common methods and attributes for project """

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        dict = {}
        dict.update(self.__dict__)
        dict.update({'__class__': self.__class__.__name__})
        dict['created_at'] = self.created_at.isoformat()
        dict['updated_at'] = self.updated_at.isoformat()
        return dict
