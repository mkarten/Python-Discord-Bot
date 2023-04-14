import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord import ui
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


playerX = 4
playerY = 9
maxX = 10
maxY = 13
gameMap = [
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
    ["🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦","🟦"],
]

def getMap():
    map = ""
    for y,row in enumerate(gameMap):
        for x,item in enumerate(row):
            if x == playerX and y == playerY:
                map += "🤡"
            else:
                map += item
        map += "\n"
    return map



@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

@tree.command(name="ping",description="Pong!")
async def ping(interaction : discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="echo",description="Echoes your message")
async def echo(interaction : discord.Interaction, message : str):
    await interaction.response.send_message(message)

@tree.command(name="exec",description="Executes a command")
async def exec(interaction : discord.Interaction, command : str):
    result = os.popen(command).read()
    if result == "":
        result = "Done."
    await interaction.response.send_message(result)

interface = []

class testView(ui.View):
    def __init__(self):
        super().__init__()
        for row in interface:
            for button in row:
                self.add_item(button)

class nonButton (ui.Button):
    def __init__(self):
        super().__init__(label="​",style=discord.ButtonStyle.gray, custom_id=str(random.randint(0,10000000)),disabled=True)

    async def callback(self, interaction : discord.Interaction):
        await interaction.response.edit_message(view=testView(),content=getMap())

class UpButton(ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.gray, custom_id="up",emoji="⬆️")

    async def callback(self, interaction : discord.Interaction):
        if playerY > 0:
            playerY -= 1
        await interaction.response.edit_message(view=testView(),content=getMap())

class DownButton(ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.gray, custom_id="down",emoji="⬇️")

    async def callback(self, interaction : discord.Interaction):
        if playerY < maxY:
            playerY += 1
        await interaction.response.edit_message(view=testView(),content=getMap())

class LeftButton(ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.gray, custom_id="left",emoji="⬅️")

    async def callback(self, interaction : discord.Interaction):
        if playerX > 0:
            playerX -= 1
        await interaction.response.edit_message(view=testView(),content=getMap())

class RightButton(ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.gray, custom_id="right",emoji="➡️")

    async def callback(self, interaction : discord.Interaction):
        if playerX < maxX:
            playerX += 1
        await interaction.response.edit_message(view=testView(),content=getMap())

class AButton(ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.gray, custom_id="a",emoji="🅰️")

    async def callback(self, interaction : discord.Interaction):
        print("A")
        await interaction.response.edit_message(view=testView())

class BButton(ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.gray, custom_id="b",emoji="🅱️")

    async def callback(self, interaction : discord.Interaction):
        print("B")
        await interaction.response.edit_message(view=testView())

interface = [
    [nonButton(),UpButton(),nonButton(),nonButton(),nonButton()],
    [LeftButton(),nonButton(),RightButton(),nonButton(),nonButton()],
    [nonButton(),DownButton(),nonButton(),nonButton(),nonButton()],
    [nonButton(),nonButton(),nonButton(),AButton(),BButton()]
]    
    
@tree.command(name="clear",description="Clears the channel")
async def clear(interaction : discord.Interaction):
    await interaction.channel.purge(limit=1000000)

@tree.command(name="ui",description="Shows a UI")
async def ui(interaction : discord.Interaction):
    await interaction.response.send_message(getMap(),view=testView())




@tree.context_menu(name="greet")
async def greet(interaction : discord.Interaction, user : discord.Member):
    await interaction.response.send_message(f"Hello {user.name}!",ephemeral=True)

def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    client.run(token)

if __name__ == "__main__":
    main()