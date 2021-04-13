#!/usr/bin/env python

import subprocess
from os import path, curdir, chdir

home_dir = path.expanduser("~")


# Gets current directory and replaces your home directory with "~"
def current_dir():
    return path.abspath(curdir).replace(home_dir, "~")


# Escapes a string by replacing spaces " " with "\s" between quotation marks
def escape_space(string):
    out = ""
    quote = False
    for letter in string:
        quote = (quote != (letter == "\""))  # quote <- quote XOR letter is "
        if quote and letter == " ":
            letter = "\s"
        out += letter
    return out


# Dictionary that holds all variables
var_dict = {}


# Handles Variables
def handle_vars(command_args):
    for i in range(len(command_args)):
        arg = command_args[i]

        # Replace variables with their value
        if arg[0] == "$":
            if arg[1:] in var_dict:
                command_args[i] = var_dict[arg[1:]]
            else:
                command_args[i] = ""

        # Add new variable
        elif "=" in arg:
            arg_split = arg.split("=")
            var_dict[arg_split[0]] = arg_split[1]


quit_flag = False

if __name__ == "__main__":
    while True:
        display_dir = "\033[34m{}\033[39m$ ".format(current_dir())  # The current directory with color
        commands = input(display_dir).rstrip('\n').split(";")

        # Repeat for all commands (multiple commands are possible with ";")
        for cmd in commands:

            cmd = escape_space(cmd)
            command_args = cmd.split(" ")

            handle_vars(command_args)

            if command_args[0] == "quit":
                quit_flag = True
                break
            elif command_args[0] == "cd":
                chdir(command_args[1])  # change execution dir
            else:
                command = " ".join(command_args).replace("\s", " ")
                shell = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                print("Hello: {}".format(shell.stdout.read().decode("UTF-8")))

        if quit_flag:
            break

    print("Shell Terminated.")