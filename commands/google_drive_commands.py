import discord
import math
import aiohttp
import magic
from commands.gdf import report as reports
from commands.gdf import locateobjects as gdfuncs
from io import BytesIO








class GoogleDriveCommands:

    def __init__(self, p: str, client: discord.Client):
        self.p = p
        self.client = client
        self.drive = gdfuncs.gauth
        self.topFolders = gdfuncs.searchForSubfolders('root')
        self.allFolders = gdfuncs.allFolders() + [('root', 'root')]
        self.files = gdfuncs.allFiles()


    async def sendFile(self, message):
        await self.tryDelMsg(message)
        name = ' '.join(message.content.split(' ')[1:])
        file = gdfuncs.searchForFileAnywhere(name)
        f = discord.File(BytesIO(file.GetContentIOBuffer(mimetype=file['mimeType']).read()), filename='{}.{}'.format(file['title'], file['mimeType'].split('/')[-1]))
        await message.channel.send(file=f)


    async def sendFileContentString(self, message):
        await self.tryDelMsg(message)
        name = ' '.join(message.content.split(' ')[1:])
        file = gdfuncs.searchForFileAnywhere(name)
        fileContent = file.GetContentString()
        i = 0
        for index in range(math.ceil(len(fileContent)/1990)):
            await message.channel.send("{}".format(fileContent[i:i+1990]))#.replace(r"\n", r"\r\n")))
            i += 1990



    async def trashFile(self, message):
        await self.tryDelMsg(message)
        name = ' '.join(message.content.split(' ')[1:])
        file = gdfuncs.searchForFileAnywhere(name)
        file.Trash()


    async def untrashFile(self, message):
        await self.tryDelMsg(message)
        name = ' '.join(message.content.split(' ')[1:])
        file = gdfuncs.searchForTrashedFiles(name)
        file.UnTrash()


    async def deleteFile(self, message):
        await self.tryDelMsg(message)
        name = ' '.join(message.content.split(' ')[1:])
        file = gdfuncs.searchForFileAnywhere(name)
        file.Delete()


    async def getFileInfo(self, message):
        await self.tryDelMsg(message)
        name = ' '.join(message.content.split(' ')[1:])
        file = gdfuncs.searchForFileAnywhere(name)
        await message.channel.send("""
    ```nim
    File Name: {}
    File Type: {}
    File Size: {} bytes   ({} KB)
    ```""".format(file['title'], file['mimeType'], int(file['fileSize']), round(int(file['fileSize'])/1024), 2))


    async def uploadTextFileFromString(self, message):
        msgcontent = message.content
        title, target = message.content.split('"')[1], message.content.split('"')[3]
        content = msgcontent[msgcontent.index(message.content.split('"')[4]):]
        for folder in self.allFolders:
            if (folder[0] in target):
                folderName, folderID = folder
                break
        file = gdfuncs.drive.CreateFile({'title': title, 'parents': [{'id': folderID}], 'mimeType': "text/plain"})
        file['description'] = f"Uploaded by:\n {message.author}"
        file.content = BytesIO(content.encode(encoding="utf-8"))
        file.Upload()
        cmptitle = "File Uploaded Successfully!"
        completion = "File Name: {}\nFile Folder: {}\nFile Type: text/plain\n".format(title, folderName)
        await message.channel.send("```nim\n{}\n\n{}```".format(cmptitle,completion))


    async def uploadFileFromURL(self, message):
        file, folderName, folderID, content, mimeType, desc = None, None, None, None, None, None
        content = message.content.split(' ')
        if(len(content)) < 4:
            await message.channel.send("Failed to upload. Too few arguments.")
            return
        url, title, target, desc = content[1], content[2], content[3], ' '.join(content[4:])
        for folder in self.allFolders:
            if (folder[0] in target):
                folderName, folderID = folder
                break
        await self.tryDelMsg(message)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    mimeType = magic.from_buffer(content[:2048], mime=True)
                else:
                    print("Failed to get url: {}\n".format(url))
                    return
        file = gdfuncs.drive.CreateFile({'title': title, 'parents': [{'id': folderID}], 'mimeType': mimeType})
        file['mimeType'] = mimeType
        file['description'] = f"Uploaded by:\n {message.author}\n---------------------------------------\n{desc}"
        file.content = BytesIO(content)
        file.Upload()
        cmptitle = "File Uploaded Successfully!"
        completion = "File Name: {}\nFile Folder: {}\nFile Type: {}\nFile Description: {}".format(title, folderName, mimeType, desc)
        await message.channel.send("```nim\n{}\n\n{}```".format(cmptitle,completion))
                    

    async def tryDelMsg(self, message):
        try:
            await message.delete()
        except Exception as e:
            print(e)




    async def search(self, message):
        buffer = []
        count = 0
        page = 1
        files = None
        target = message.content.split(' ')[1:]
        # -----------------------------------------------------------------------------------------------
        await self.tryDelMsg(message)
        # -----------------------------------------------------------------------------------------------
        for folder in self.allFolders:
            if (folder[0] in target):
                files = gdfuncs.searchForAllInFolder(folder[1])
                break
        if not (files):
            await reports.error("invalid Folder Given!", "You searched for ``{}``".format(' '.join(target) if target != [] else "an empty folder."), message)
            return
        for file in files:
            count +=1
            buffer.append("{} {}".format(f"\n{count}) {file[0]} "[:29].ljust(30), f"|  .{file[1].split('/')[1]}"[:30]))
        # -----------------------------------------------------------------------------------------------
        e = discord.Embed(title="Searching")
        e.add_field(name=f"Page 1 of {math.ceil(count / 20)}  \({count} Items total\)",
                    value="```nim\nTitles:                        File Type:\n--------------------------------------------------------" + 
                    ' '.join(buffer[((page - 1) * 20): (page * 20)]) + "```")
        msg = await message.channel.send(embed=e)
        # -----------------------------------------------------------------------------------------------
        def listenmsg(m):
            return m.content.split(' ')[0] in ["up", "down", f'{self.p}search'] and m.author == self.client.user
        # -----------------------------------------------------------------------------------------------
        while True:
            try:
                m = await self.client.wait_for('message', check=listenmsg)
                if m.content == 'up':
                    await m.delete()
                    if page < math.ceil(count / 20):
                        page += 1
                    else:
                        pass
                    await self.searchemb(page, buffer, count, msg, message)
                elif m.content == 'down':
                    await m.delete()
                    if page > 1:
                        page -= 1
                    else:
                        pass
                    await self.searchemb(page, buffer, count, msg, message)
                elif m.content.split(' ')[0] == f'{self.p}search':
                    await msg.delete()
                    return
            except Exception as e:
                print(e)
        # -----------------------------------------------------------------------------------------------
    async def searchemb(page, buffer, count, msg, message):
        e = discord.Embed(title="Searching")
        e.add_field(name=f"Page {page} of {math.ceil(count / 20)}  \({count} Items total\)",
                    value="```nim\nTitles:                        File Type:\n--------------------------------------------------------" + ' '.join(
                        buffer[((page - 1) * 20): (page * 20)]) + "```")
        await msg.edit(embed=e)
        return
    # -----------------------------------------------------------------------------------------------


    async def advertMsg(self, message):
        content = message.content.split(' ')
        await self.tryDelMsg(message)
        if (len(content) > 1):
            await message.channel.send("https://github.com/NextGEN-Organization/{}".format(content[1]))
        else:
            await message.channel.send("https://github.com/NextGEN-Organization/")