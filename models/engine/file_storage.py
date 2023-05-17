#!/usr/bin/python3
"""This module defines a class to manage file storage for airbnb clone"""
import json


class FileStorage:
    """This class manages storage of airbnb models in JSON format"""

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns a dictionary of models currently in storage"""
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize dictionary into a json file"""
        with open(FileStorage.__file_path, 'w') as f:
            tmp_dict = {}
            tmp_dict.update(FileStorage.__objects)
            for key, value in tmp_dict.items():
                tmp_dict[key] = value.to_dict()
            json.dump(tmp_dict, f)

    def reload(self):
        """ Deserialize and create instance of object saved in json file"""
        try:
            from models.base_model import BaseModel
            from models import storage
            from models.user import User
            from models.place import Place
            from models.state import State
            from models.city import City
            from models.amenity import Amenity
            from models.review import Review
            with open(FileStorage.__file_path, 'r') as f:
                tmp_dict = json.load(f)
                for key, value in tmp_dict.items():
                    tmp_obj = eval(value['__class__'] + "(**value)")
                    FileStorage.__objects[key] = tmp_obj
        except FileNotFoundError:
            pass
