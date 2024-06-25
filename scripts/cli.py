from common import *
from show import *
from help import *
from error import *

def cli():
    try:
        running = True
        while running:
            command = input("coyote~$ ").lower().strip()
            if command == "":
                pass
            else:
                args = command.split()
                root = args[0]
                if command in help_commands:
                    help("top", args)
                elif command in exit_commands:
                    running = False
                    exit()
                elif root in util_commands:
                    pshell_input = pshell_decoder(command)
                    if pshell_input is not None:
                        newline()
                        print(pshell_input)
                        newline()
                        pass
                    else:
                        pass
                # 'show' command processing
                elif root == "show":
                    try:
                        for cmd in show_commands:
                            if cmd == command: 
                                pshell_input = pshell_decoder(show_commands.get(cmd))
                                if cmd == "show logging":
                                    paginate_output(pshell_input)
                                    break
                                elif cmd == "show tcp provider":
                                    newline()
                                    print(pshell_input)
                                    newline()
                                    pass
                                elif cmd == "show ip public":
                                    if pshell_input is not None:
                                        newline()
                                        print(pshell_input)
                                        newline()
                                        pass
                                    else:
                                        pass
                                else:
                                    parse_json(pshell_input, show_params.get(cmd))
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
    except:
        pass
