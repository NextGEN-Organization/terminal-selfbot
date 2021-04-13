#!/usr/bin/env python
import subprocess
import asyncio
import time
import concurrent.futures
from shlex import *
from helper_classes.helper_functions import *
from os import path, curdir, chdir

# import nest_asyncio
# nest_asyncio.apply()

class TerminalCommands:
    def __init__(self, loop=asyncio.get_event_loop()):
        self.loop = loop
        self._async = self.loop.run_until_complete
        self.terminals = []
        self.term_index = -1


    async def monitorResults(self, index, channel):
        last_stdout = None
        last_stderr = None
        term = self.terminals[index]
        while True:
            try:

                if term.quit_flag == True:
                    break

                if self.terminals == [] or term.stdout == None:
                    await asyncio.sleep(0.5)
                    continue
            
                stdout = term.stdout
                stderr = term.stderr

                if last_stdout == stdout and last_stderr == stderr:
                    await asyncio.sleep(0.5)
                    continue

                last_stdout = stdout
                last_stderr = stderr

                results = "```\nOutput:\n{}\n``````\nErrors:\n{}```".format(stdout, stderr if stderr != "" else "there were no errors.")
                await channel.send(results[0:1990] + "\n\n...```" if len(results) > 1990 else results)

            except asyncio.CancelledError:
                print("done waiting for results.")
                return


    async def createTerminal(self, message, **kwargs):
        if len(message.content.split(' ')) > 1:
            content = ' '.join(message.content.split(' ')[1:])
        else:
            content = None


        def test(content: "list[str]"):
            cmd = content
            terminal = SingleTerminal(cmd)
            self.terminals.append(terminal)
            self.term_index+=1
            terminal.create_console()
            self.terminals.remove(terminal)
            self.term_index-=1
            return
        

        asyncio.create_task(self.monitorResults(self.term_index + 1, message.channel))
        with concurrent.futures.ThreadPoolExecutor() as pool:
            await self.loop.run_in_executor(pool, test, content)
            
        


    async def inputToTerminal(self, message):
        self.terminals[self.term_index].set_commands(' '.join(message.content.split(' ')[1:]))
        #monitor = asyncio.ensure_future(self.monitorResults(self.term_index, message.channel))


    async def monitorTerminals(self, message):
        await message.channel.send("```There are {} terminals.\nCurrently Running Commands: {}```".format(len(self.terminals), ", ".join([terminal.commands for terminal in self.terminals]) if self.terminals != [] else "No commands running. All terminals closed." ))


    async def get_current_stdout(self, message):
        term = self.terminals[self.term_index]
        results = "```\nLast Command Ran: {}\n``````\nOutput:\n{}\n``````\nErrors:\n{}```".format(term.commands, term.stdout, term.stderr if term.stderr != "" else "there were no errors.")
        await message.channel.send(results[0:1990] + "\n\n...```" if len(results) > 1990 else results)

class SingleTerminal:
    def __init__(self, commands=None):
        self.commands = commands
        self.home_dir = path.expanduser("~")
        self.var_dict = {}
        self.quit_flag = False
        self.stdout = None
        self.stderr = None


    def set_commands(self, commands: str):
        self.commands = commands


    # Gets current directory and replaces your home directory with "~"
    def current_dir(self):
        return path.abspath(curdir).replace(self.home_dir, "~")


    # Escapes a string by replacing spaces " " with "\s" between quotation marks
    def escape_space(self, string):
        out = ""
        quote = False
        for letter in string:
            quote = (quote != (letter == "\""))  # quote <- quote XOR letter is "
            if quote and letter == " ":
                letter = "\s"
            out += letter
        return out


    # Dictionary that holds all variables
   

    # Handles Variables
    def handle_vars(self, command_args):
        for i in range(len(command_args)):
            arg = command_args[i]

            # Replace variables with their value
            if arg[0] == "$":
                if arg[1:] in self.var_dict:
                    command_args[i] = self.var_dict[arg[1:]]
                else:
                    command_args[i] = ""

            # Add new variable
            elif "=" in arg:
                arg_split = arg.split("=")
                self.var_dict[arg_split[0]] = arg_split[1]


    def create_console(self):
        while True:
            if (self.commands == None):
                time.sleep(0.5)
                continue

            #display_dir = "\033[34m{}\033[39m$ ".format(self.current_dir())  # The current directory with color
            commands = self.commands.split(";")
            # Repeat for all commands (multiple commands are possible with ";")
            for cmd in commands:
                cmd = cmd.lstrip(' ')
                cmd = self.escape_space(cmd)
                command_args = cmd.split(" ")

                self.handle_vars(command_args)

                if command_args[0] == "quit":
                    self.quit_flag = True
                    break
                elif command_args[0] == "cd":
                    chdir(command_args[1])  # change execution dir
                else:
                    command = " ".join(command_args).replace("\s", " ")
                    shell = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    self.stdout = shell.stdout.read().decode("UTF-8").rstrip('\n')
                    self.stderr = shell.stderr.read().decode("UTF-8").rstrip('\n')

            #self.stdout = None
            #self.stderr = None
            self.commands = None
            

            if self.quit_flag:
                break

        print("Shell Terminated.")