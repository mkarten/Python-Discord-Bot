import os
from dotenv import load_dotenv
import discord
from discord.ui import Button, View
from discord import app_commands
from history import History
from Chat import chat, registerApi
from tree import parse_json_to_tree, Tree
import jsonpickle

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
history = History("./history.json")
jsonPath = "tree.json"
conversationTrees = dict[str,Tree]()


chats = dict[int,chat]()

def exportChats(chatArray):
    return jsonpickle.encode(chatArray,unpicklable=False)

def loadChats(jsonChats):
    return jsonpickle.decode(jsonChats)

def accessUHistory(userID : str)->list[str]:
    return history.AccessUserHistory(userID)

def addHistory(userID : str, message : str):
    history.AddUserHistory(userID, message)

def lastCommand(userID : str)->str:
    return history.GetLastCommand(userID)

def currentCommand(userID : str)->str:
    return history.GetCurrentCommand(userID)

def goBack(userID : str)->str:
    history.GoBackward(userID)

def goForward(userID : str)->str:
    history.GoForward(userID)

def clearHistory(userID : str)->str:
    history.Clear(userID)

historyExclude = ["go-back-history","go-forward-history","last-command","current-command","clear-history","show-complete-history"]

@client.event
async def on_interaction(interaction : discord.Interaction):
    if interaction.type == discord.InteractionType.application_command:
        if interaction.data["name"] not in historyExclude:
            addHistory(interaction.user.id, interaction.data["name"])


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

def yeildTree(userID : int):
    if userID not in conversationTrees:
        with open(jsonPath, "r") as f:
            conversationTrees[userID] = parse_json_to_tree(f.read())
    return conversationTrees[userID]

async def resetConversation(interaction : discord.Interaction):
    userID = interaction.user.id
    conversationTree = yeildTree(userID)
    conversationTree.Reset()
    tempView = View()
    for option in conversationTree.ListOptions():
        # create a button that is clickable only by the user who started the command and advances the conversation
        tempButton = Button(label=option,style=discord.ButtonStyle.primary,custom_id=option,disabled=False)
        tempButton.callback = callback
        tempView.add_item(tempButton)
    restart = Button(label="Restart",style=discord.ButtonStyle.primary,custom_id="restart",disabled=False)
    restart.callback = resetConversation
    exit = Button(label="Exit",style=discord.ButtonStyle.primary,custom_id="exit",disabled=False)
    exit.callback = exitConversation
    tempView.add_item(restart)
    tempView.add_item(exit)
    # end the interaction
    await interaction.response.defer()
    await interaction.message.edit(content=conversationTree.GetQuestion(),view=tempView)

async def exitConversation(interaction : discord.Interaction):
    userID = interaction.user.id
    conversationTree = yeildTree(userID)
    conversationTree.Reset()
    tempView = View()
    await interaction.response.defer()
    await interaction.message.delete()


async def callback(interaction : discord.Interaction):
    userID = interaction.user.id
    conversationTree = yeildTree(userID)
    tempView = View()
    if conversationTree.ChooseOption(interaction.data["custom_id"]):
        for option in conversationTree.ListOptions():
            # create a button that is clickable only by the user who started the command and advances the conversation
            tempButton = Button(label=option,style=discord.ButtonStyle.primary,custom_id=option,disabled=False)
            tempButton.callback = callback
            tempView.add_item(tempButton)
    restart = Button(label="Restart",style=discord.ButtonStyle.primary,custom_id="restart",disabled=False)
    restart.callback = resetConversation
    exit = Button(label="Exit",style=discord.ButtonStyle.primary,custom_id="exit",disabled=False)
    exit.callback = exitConversation
    tempView.add_item(restart)
    tempView.add_item(exit)
    await interaction.response.defer()
    await interaction.message.edit(content=conversationTree.GetQuestion(),view=tempView)


@tree.command(name="speak-about",description="Starts the conversation")
async def startConversation(interaction : discord.Interaction):
    userID = interaction.user.id
    conversationTree = yeildTree(userID)
    tempView = View()
    for option in conversationTree.ListOptions():
        # create a button that is clickable only by the user who started the command and advances the conversation
        tempButton = Button(label=option,style=discord.ButtonStyle.primary,custom_id=option,disabled=False)
        tempButton.callback = callback
        tempView.add_item(tempButton)
    restart = Button(label="Restart",style=discord.ButtonStyle.primary,custom_id="restart",disabled=False)
    restart.callback = resetConversation
    exit = Button(label="Exit",style=discord.ButtonStyle.primary,custom_id="exit",disabled=False)
    exit.callback = exitConversation
    tempView.add_item(restart)
    tempView.add_item(exit)
    await interaction.response.defer()
    await interaction.followup.send(conversationTree.GetQuestion(),view=tempView)



@tree.command(name="last-command",description="Shows the last command used by the user")
async def lastUCommand(interaction : discord.Interaction):
    userID = interaction.user.id
    await interaction.response.send_message(lastCommand(userID),ephemeral=True)

@tree.command(name="current-command",description="Shows the current command used by the user")
async def currentUCommand(interaction : discord.Interaction):
    userID = interaction.user.id
    await interaction.response.send_message(currentCommand(userID),ephemeral=True)

@tree.command(name="go-backward-history",description="Goes back to the previous command used by the user")
async def goBUCommand(interaction : discord.Interaction):
    userID = interaction.user.id
    goBack(userID)
    await interaction.response.send_message(currentCommand(userID),ephemeral=True)

@tree.command(name="go-forward-history",description="Goes forward to the next command used by the user")
async def goFUCommand(interaction : discord.Interaction):
    userID = interaction.user.id
    goForward(userID)
    await interaction.response.send_message(currentCommand(userID),ephemeral=True)

@tree.command(name="clear-history",description="Clears the user command history")
async def clearUHistory(interaction : discord.Interaction):
    userID = interaction.user.id
    clearHistory(userID)
    await interaction.response.send_message("cleared the user history",ephemeral=True)

@tree.command(name="show-complete-history",description="Accesses the user command history")
async def accessUserHistory(interaction : discord.Interaction):
    channelID = interaction.channel.id
    userID = interaction.user.id
    history = accessUHistory(userID)
    #adds \n to the end of each element in the list
    history = [x + "\n" for x in history]
    await interaction.response.send_message("here is the user history : \n" + "".join(history),ephemeral=True)

@tree.command(name="ping",description="Pong!")
async def ping(interaction : discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="echo",description="Echoes your message")
async def echo(interaction : discord.Interaction, message : str):
    await interaction.response.send_message(message)

    
@tree.command(name="clear",description="Clears the channel")
async def clear(interaction : discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.purge(limit=10000)
    await interaction.followup.send("cleared the channel",ephemeral=True)

@tree.command(name="converse",description="a channel based conversation system with chatGPT")
async def askGPT(interaction : discord.Interaction, question : str):
    channelID = interaction.channel.id
    if channelID not in chats:
        chats[channelID] = chat()
    currentChat: chat = chats[channelID]
    await interaction.response.send_message("waiting for response...")
    response,cost = currentChat.askGpt(question)
    msg = await interaction.original_response()
    await msg.edit(content=f"you ask : {question}\nHere is the answer : {response}\n\nIt costed {cost:.6f} $")

@tree.command(name="ask",description="Asks a question to the bot ans GPT-3 will answer")
async def ask(interaction : discord.Interaction, question : str):
    await interaction.response.send_message("waiting for response...")
    tempchat = chat()
    response,cost = tempchat.askGpt(question)
    msg = await interaction.original_response()
    await msg.edit(content=f"you ask : {question}\nHere is the answer : {response}\n\nIt costed {cost:.6f} $")


@tree.command(name="rickroll",description="Rickrolls a user")
async def rickroll(interaction : discord.Interaction, user : discord.Member):
    #send a rickroll gif to the user privately
    await user.send("https://tenor.com/bEWOf.gif")
    await interaction.response.send_message(f"Rickrolled {user.name}!",ephemeral=True)

@tree.command(name="troll",description="Trolls a user")
async def troll(interaction : discord.Interaction, user : discord.Member):
    await interaction.response.send_message(f"J'tai trollé <@{user.id}>!")

@tree.context_menu(name="greet")
async def greet(interaction : discord.Interaction, user : discord.Member):
    await interaction.response.send_message(f"Hello {user.name}!",ephemeral=True)

def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    OpenAISecret = os.getenv("OPENAI_SECRET")
    OpenAIOrganization = os.getenv("OPENAI_ORGANIZATION")
    registerApi(OpenAISecret,OpenAIOrganization)
    client.run(token)

if __name__ == "__main__":
    main()