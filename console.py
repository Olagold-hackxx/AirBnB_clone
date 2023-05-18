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
    advance_cmds = ['all', 'count', 'show', 'destroy', 'update']
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

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class instance of any available type class")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        cmds = args.split(" ")
        if len(cmds) < 2:
            ret_val = self.handle_cmds(args)
            if ret_val:
                print("** instance id missing **")
            return
        key = self.handle_cmds(args)
        if key is not None:
            all_objects = storage.all()
            try:
                print(all_objects[key])
            except KeyError:
                print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        cmds = args.split(" ")
        if len(cmds) < 2:
            ret_val = self.handle_cmds(args)
            if ret_val:
                print("** instance id missing **")
            return
        key = self.handle_cmds(args)
        if key is not None:
            all_objects = storage.all()
            try:
                del all_objects[key]
                storage.save()
            except KeyError:
                print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def handle_cmds(self, args):
        if len(args.split(" ")) >= 2:
            cmd_list = args.split(" ")
            if not cmd_list[0]:
                print("** class name missing **")
                return
            elif cmd_list[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
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
            else:
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

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_update(self, args):
        cmds = args.split(" ")
        if len(cmds) < 2:
            ret_val = self.handle_cmds(args)
            if ret_val:
                print("** instance id missing **")
            return
        key = self.handle_cmds(args)
        if key is not None:
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

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

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

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.advance_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop


if __name__ == '__main__':
    HBNBCommand().cmdloop()
