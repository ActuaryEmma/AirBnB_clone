#!/usr/bin/env python3
"""
contains the entry point of the command interpreter
"""
import cmd
import sys
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage


class HBNBCommand(cmd.Cmd):
    """contains the entry point of the command interpreter"""
    prompt = '(hbnb)'
    classls = ["BaseModel"]

    @staticmethod
    def error_message(caller, arg):
        list_message = ["** class name missing **",
                        "** class doesn't exist **",
                        "** instance id missing **",
                        "** no instance found **"]
        if not arg:
            print(list_message[0])
        elif caller == 'show' and arg.split()[0] not in HBNBCommand.classls:
            print(list_message[1])
        elif caller == 'create' and arg not in HBNBCommand.classls:
            print(list_message[1])
        elif caller == 'destroy' and arg.split()[0] not in HBNBCommand.classls:
            print(list_message[1])
        elif caller == 'all' and arg not in HBNBCommand.classls:
            print(list_message[1])
        elif caller == 'update' and arg.split()[0] not in HBNBCommand.classls:
            print(list_message[1])
        elif caller == "show" and len(arg.split()) < 2:
            print(list_message[2])
        elif caller == "destroy" and len(arg.split()) < 2:
            print(list_message[2])
        elif caller == "update" and len(arg.split()) < 2:
            print(list_message[2])
        else:
            return 0

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it"""
        if HBNBCommand.error_message("create", arg) is None:
            return
        else:
            base = BaseModel()
            base.save()
            base_id = base.id
            print(base_id)

    def do_show(self, arg):
        """string representation of an instance based on the class name / id"""
        objects = {}
        args = arg.split()
        if HBNBCommand.error_message("show", arg) is None:
            return
        else:
            objects = FileStorage().all()
            key = f"{args[0]}.{args[1]}"
            if (key not in tuple(objects.keys())):
                print("** no instance found **")
            else:
                print(objects.get(key))

    def do_destroy(self, arg):
        """ Deletes an instance based on the class name and id
            (save the change into the JSON file)
        """
        args = arg.split()
        objects = {}
        if HBNBCommand.error_message("destroy", arg) is None:
            return
        else:
            objects = FileStorage().all()
            key = f"{args[0]}.{args[1]}"
            if (key not in tuple(objects.keys())):
                print("** no instance found **")
            else:
                del objects[key]
                storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances based or
           not on the class name.
        """
        objects = {}
        if HBNBCommand.error_message("all", arg) is None:
            return
        else:
            objects = FileStorage().all()
            class_objects = []
            for obj in objects.values():
                if type(obj).__name__ == arg:
                    description = str(obj)
                    class_objects.append(description)
            print(class_objects)

    def do_update(self, arg):
        objects = {}
        args = arg.split()
        if HBNBCommand.error_message("update", arg) is None:
            return (None)
        objects = FileStorage().all()
        key = f"{args[0]}.{args[1]}"

        if key not in objects:
            print("** no instance found **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            obj = objects[key]
            key_name = args[2]
            value_name = args[3]
            setattr(obj, key_name, value_name)
            obj.save()

    def emptyline(self):
        """empty file should execute nothing"""
        pass

    def do_EOF(self, line):
        """when you ctrl + D you are able to exit the file"""
        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def postloop(self):
        """print a new line after you exit the program"""
        print()


if __name__ == "__main__":
    my_cmd = HBNBCommand()
    my_cmd.cmdloop()
