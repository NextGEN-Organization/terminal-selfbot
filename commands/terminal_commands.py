import subprocess
import asyncio
import time
import concurrent.futures
from shlex import *
from helper_classes.helper_functions import *

import nest_asyncio
nest_asyncio.apply()


class TerminalCommands:
    def __init__(self, loop=asyncio.get_event_loop()):
        self.loop = loop
        self._async = self.loop.run_until_complete
        self.terminals = []
        self.term_index = -1


    async def createTerminal(self, message, **kwargs):
        if len(message.content.split(' ')) > 1:
            content = ' '.join(message.content.split(' ')[1:])
        else:
            content = None
        


        def test(content: "list[str]"):
            cmd = ["sh", "-c"] 
            cmd.append(content)
            cmd = content
            command = SingleTerminal(cmd)
            self.terminals.append()
            return command.stdout.read(), command.stderr.read()
        

        with concurrent.futures.ThreadPoolExecutor() as pool:
            stdout, stderr = await self.loop.run_in_executor(pool, test, content)
            await message.channel.send("```\n{}\n```".format(stdout))
            await message.channel.send(("Error: " + stderr) if stderr != "" else "there were no errors.")



    async def runProcess(self, message, **kwargs):
        content = ' '.join(message.content.split(' ')[1:])



    async def newRunProcess(self, message, **kwargs):
        term = AsyncSingleTerminal(message)
        self.term_index +=1
        print(self.term_index)
        self.terminals.append(term)
        await message.channel.send("```\n{}\n```".format((await term.read_stdout()).decode()))

    
    async def inputToProcess(self, message):
        try:
            term_to_use = int(message.content.split(' ')[1])
        except Exception as e:
            print(e)
            return
        await self.terminals[term_to_use].write_stdin(' '.join(message.content.split(' ')[2:]))
        stdout, stderr = await self.terminals[term_to_use].reportInfo()

        stdout = stdout.decode('ascii').rstrip()
        #await message.channel.send("```\n{}\n```".format((stdout)))


    




class AsyncSingleTerminal:
    def __init__(self, message, process_input=None, write_timeout=15, loop=asyncio.get_event_loop()):
        self.loop = loop
        self._async = self.loop.run_until_complete
        self.context = message
        self.input = process_input
        self.write_timeout = write_timeout
        self.process = self._async(self.createSubprocess())


    async def createSubprocess(self):
        command = ' '.join(self.context.content.split(' ')[1:])
        #*split(command)
        return await asyncio.create_subprocess_exec(*split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    async def killSubprocess(self):
        return await self.process.wait()


    async def reportInfo(self):
        stdout = await self.read_stdout()
        stderr = await self.read_stderr()
        print("stdout: {}\nstderr: {}".format(stdout, stderr))
        return (stdout, stderr)




    async def write_stdin(self, command: str):
        #async with self.process.stdin.open(mode='wb') as stdin:
        #    await stdin.write(command.encode("utf-8"))
        self.process.stdin.write(command.encode("utf-8"))
        await self.process.stdin.drain()


    async def read_stdout(self):
        #async with self.process.stdout.open(mode='r') as stdout:
        #    return await stdout.read()
        return await self.process.stdout.read()
    
    async def read_stderr(self):
        #async with self.process.stderr.open(mode='r') as stderr:
        #    return await stderr.read()
        return await self.process.stderr.read()





class SingleTerminal:
    def __init__(self, command: str, process_input=None, write_timeout=15):
        self.command = command
        self.input = process_input
        self.write_timeout = write_timeout
        self.process = self.createSubprocess()


    def createSubprocess(self):
        self.process = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
        

    def write_pipe(self, content: str):
        return self.process.stdin.write(content)
        return self.process.communicate(content, timeout=self.write_timeout)


    def read_stdout(self):
        return self.process.stdout.read()
        return self.process.communicate()


    def read_stderr(self):
        return self.process.stderr.read()

    



    
        



if (__name__ == "__main__"):
    tc = TerminalCommands()