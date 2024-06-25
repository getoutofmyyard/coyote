from show import show_commands
from common import *
from error import *

help_commands = [
        "help",
        "?",
        ]

exit_commands = [
        "exit",
        "quit",
        "leave",
        "bye",
        "end",
        ]

def help_show(arg, command):
    level = len(command)
    if " ".join(command) == "show" or level == 2:
        newline()

        # Keep a list of unique commands
        # based on contents of show.p

        context_list = []

        for option in show_commands:

            # Split each available command into an arra
            # in order to contextualize help per level

            split_option = option.split()

            # "notfound" is the final value in the command list
            # in show.p

            if option != "notfound":
                context = f"{split_option[0]} {split_option[1]}"
                if context not in context_list:
                    context_list.append(context)
                else:
                    pass
            else:
                pass

        if " ".join(command) in context_list:
            # Print appropriate output for incomplete commands
            for line in show_commands:
                if " ".join(command) in line:
                    print(line)
                else:
                    pass
            newline()

        else:
            # Print list of commands as help output
            for line in context_list:
                print(line)

            newline()

    elif level == 3:
        newline()

        if command[2] != "?" and command[2] != "help":
            error("unknown_command")

        context_list = []

        for option in show_commands:

            # Split each available command into an arra
            # in order to contextualize help per level

            split_option = option.split()

            # "notfound" is the final value in the command list
            # in show.p
            if option != "notfound" and len(split_option) == 3:
                context = f"{split_option[0]} {split_option[1]} {split_option[2]}"
                if context not in context_list:
                    context_list.append(context)
                else:
                    pass
            else:
                pass


        for item in context_list:
            split_item = item.split()
            if split_item[0] == command[0] and \
               split_item[1] == command[1] and \
               split_item[2] != command[2]:
               print(item)

        newline()

    else:
            pass

def help_top():
    print(r"""
arp    - configure arp
help   - show help
ip     - configure ipv4 addressing
ipv6   - configure ipv6 addressing
show   - show info and stats
tcp    - configure tcp
    """)

def help(arg, command):

    if arg == "top":
        help_top()
    elif arg == "show":
        help_show(arg, command)
    else:
        error("unknown_command")


