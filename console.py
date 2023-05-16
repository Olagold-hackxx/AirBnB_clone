#!/usr/bin/python3
"""
Command line console / interpreter for Airbnb clone project
"""
import cmd
import sys

class HBNBCommand(cmd.Cmd):
    """Command intepreter"""

    prompt = '(hbnb)'

    def do_quit(self, arg):
        """Exit console"""
        sys.exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Quit command to exit console\n")

    def do_EOF(self, arg):
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