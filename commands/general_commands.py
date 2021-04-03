from helper_classes import helper_functions as hf
from fake_useragent import UserAgent
import asyncio
ua = UserAgent()

class GeneralCommands:
    def __init__(self, token, useragent=ua.chrome, cookies=None, loop=asyncio.get_event_loop()):
        self.loop = loop
        self._async = self.loop.run_until_complete
        self.token = token
        self.useragent = useragent
        self.basic_auth_header = {'Authorization': token, 'User-Agent': self.useragent, 'X-Super-Properties': self._async(hf.getSuperProp(self.useragent))}
        if (cookies != None):
            self.basic_auth_header.update({'cookie': cookies})


    async def helpMsg(self, message):
        await message.channel.send("Helped!")


    async def errorMsg(self, message):
        await message.channel.send("You did not send a correct command.")

