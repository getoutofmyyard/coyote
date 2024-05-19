from common import *
from show import *
from help import *
from error import *

def cli():

    try:

        loop = True
        while loop == True:

            command = input("coyote~$ ").lower().strip()

            if command == "":
                pass

            else:
                args = command.split()
                root = args[0]

                if command in help_commands:
                    help("top", args)
                elif command in exit_commands:
                    loop = False
                    exit()
                elif root == "show":
                    try:
                        for cmd in show_commands:
                            if cmd == command: 
                                pshell_decoder(show_commands.get(cmd))
                                break
                            elif cmd == "notfound":
                                help("show", args)
                                break
                            else:
                                pass
                    except:
                        pass
                else:
                    pass

    except Exception:
        print(Exception)
