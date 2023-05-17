#!/usr/bin/python3

"""
Module contain class `Basemodel` that
defines all common attributes/methods for other classess
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """ Class that defines all common methods and attributes for project """

    def __init__(self, *args, **kwargs):
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """String representation of the class"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Update date and time"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Return a dictionary containing all keys/values of
        __dict__ of the instance
        """
        dict = {}
        dict.update(self.__dict__)
        dict.update({'__class__': self.__class__.__name__})
        dict['created_at'] = self.created_at.isoformat()
        dict['updated_at'] = self.updated_at.isoformat()
        return dict
