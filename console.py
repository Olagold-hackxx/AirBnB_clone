#!/usr/bin/python3
"""
Command line console / interpreter for Airbnb clone project
"""
import cmd
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command intepreter"""

    prompt = '(hbnb)'
    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    attribute_types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def do_create(self, args):
        """Create class instance"""
        condition = self.handle_cmds(args)
        if condition:
            new_instance = HBNBCommand.classes[args]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, args):
        key = self.handle_cmds(args)
        all_objects = storage.all()
        try:
            print(all_objects[key])
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        key = self.handle_cmds(args)
        all_objects = storage.all()
        try:
            del all_objects[key]
        except KeyError:
            print("** no instance found **")

    def handle_cmds(self, args):
        if len(args.split(" ")) >= 2:
            cmd_list = args.split(" ")
            if not cmd_list[0]:
                print("** class name missing **")
                return
            elif cmd_list[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            if not cmd_list[1]:
                print("** instance id missing **")
                return
            key = cmd_list[0] + "." + cmd_list[1]
            return key
        elif len(args.split(" ")) == 1:
            if not args:
                print("** class name missing **")
                return
            elif args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            return True

    def do_all(self, args):
        all_objects = storage.all()
        list_objects = []
        if args:
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for key, value in all_objects.items():
                if key.split(".")[0] == args:
                    list_objects.append(str(value))
        else:
            for key, value in all_objects.items():
                list_objects.append(str(value))
        print(list_objects)

    def do_update(self, args):
        cmds = args.split(" ")
        key = self.handle_cmds(args)
        all_objects = storage.all()
        if key in all_objects.keys():
            if len(cmds) == 2:
                print("** attribute name missing **")
            elif len(cmds) == 3:
                print("** value missing **")
            else:
                if cmds[2] in self.attribute_types.keys():
                    cmds[3] = self.attribute_types[cmds[2]](cmds[3])
                if cmds[3][0] == '"' and cmds[3][-1] == '"':
                    cmds[3] = cmds[3][1:-1]
                all_objects[key].__dict__.update({cmds[2]: cmds[3]})
                all_objects[key].save()
        else:
            print("** no instance found **")

    def do_quit(self, args):
        """Exit console"""
        sys.exit()

    def do_exit(self, args):
        """Exit console"""
        sys.exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Quit command to exit console\n")

    def help_exit(self):
        """ Prints the help documentation for quit  """
        print("Quit command to exit console\n")

    def do_EOF(self, argss):
        """ Handles EOF to exit program """
        print()
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
