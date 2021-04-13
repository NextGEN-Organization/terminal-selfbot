import discord
import random


async def success(cmptitle, completion, message):
    author = message.author
    authicon = author.avatar_url
    guild = message.guild
    content = message.content.split(' ')
    mentions = []
    i = 0
    for arg in content:
        if arg.startswith("<@!") == True:
            member = message.guild.get_member(int(arg[3:-1]))
            mentions.append(f"@{member.name}")
            i += 1

        if arg.startswith("<@&") == True:
            role = message.guild.get_role(int(arg[3:-1]))
            mentions.append(f"@{role.name}")
            i += 1

    parsec = ' '.join(content[1:])
    Color = random.randrange(0, 16777216)
    e = discord.Embed(title=f"{cmptitle}", description=f"{completion}", color=Color)
    e.set_thumbnail(url="https://media.discordapp.net/attachments/775855999042322455/780241023120441374/skelly_2.png")
    if i == 0:
        e.set_footer(text="Command by: " + str(author) + f"\nCommand: {' '.join(content)}", icon_url=str(authicon))
    if i > 0:
        e.set_footer(text="Command by: " + str(author) + f"\nCommand: {content[0]} {' '.join(mentions)}",
                     icon_url=str(authicon))
    await message.channel.send(embed=e)
    return


async def error(cmdname, errmsg, message):
    author = message.author
    authicon = author.avatar_url
    guild = message.guild
    content = message.content.split(' ')
    mentions = []
    i = 0
    for arg in content:
        if arg.startswith("<@!") == True:
            member = message.guild.get_member(int(arg[3:-1]))
            mentions.append(f"@{member.name}")
            i += 1

        if arg.startswith("<@&") == True:
            role = message.guild.get_role(int(arg[3:-1]))
            mentions.append(f"@{role.name}")
            i += 1
    Color = random.randrange(0, 16777216)
    e = discord.Embed(title=f"{cmdname}", description=f"{errmsg}", color=Color)
    e.set_thumbnail(url="https://media.discordapp.net/attachments/775855999042322455/780241023120441374/skelly_2.png")
    if i == 0:
        e.set_footer(text="Command by: " + str(author) + f"\nCommand: {' '.join(content)}", icon_url=str(authicon))
    if i > 0:
        e.set_footer(text="Command by: " + str(author) + f"\nCommand: {content[0]} {' '.join(mentions)}",
                     icon_url=str(authicon))
    await message.channel.send(embed=e)
    return