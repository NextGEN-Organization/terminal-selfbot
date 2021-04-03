import subprocess
import asyncio


class TerminalCommands:
    def __init__(self, loop=asyncio.get_event_loop()):
        self.loop = loop
        self._async = self.loop.run_until_complete


    async def runProcess(self, message, **kwargs):
        useless_cat_call = subprocess.run(["cat"], stdout=subprocess.PIPE, text=True, input="Hello from the other side")
        await message.channel.send(useless_cat_call.stdout)