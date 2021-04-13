import discord
import asyncio
from fake_useragent import UserAgent


from config import local_config as cfg
from commands.general_commands import GeneralCommands as gc
from commands.terminal_commands import TerminalCommands as tc
from commands.google_drive_commands import GoogleDriveCommands as gdc

ua = UserAgent()





class MyClient(discord.Client):
    def __init__(self, loop, token, **kwargs):
        super().__init__(loop=loop)
        self.token = token
        self.gc = gc(token, **kwargs)
        self.tc = tc()
        self.gdc = gdc(cfg.prefix, self)

    
    async def on_message(self, message):
        if (message.author.id in cfg.authUserList) and (message.content.startswith(cfg.prefix)):
            switch = {
                # general commands
                "help": self.gc.helpMsg,

                # terminal commands
                "run": self.tc.createTerminal,
                "input": self.tc.inputToTerminal,
                "tinfo": self.tc.monitorTerminals,
                "lastout": self.tc.get_current_stdout,

                # google drive commands
                "search": self.gdc.search,
                "grab": self.gdc.sendFile,
                "fileinfo": self.gdc.getFileInfo,
                
            }
            await switch.get(message.content.split(' ')[0].replace(cfg.prefix, ""), self.gc.errorMsg)(message)


    async def on_connect(self):
        print(self.user.name)


def main():
    loop = asyncio.get_event_loop()
    client = MyClient(loop, cfg.masterToken, useragent=ua.chrome)
    client.run(cfg.masterToken, bot=False)



if (__name__ == "__main__"):
    main()
        