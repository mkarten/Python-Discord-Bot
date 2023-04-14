import os
from dotenv import load_dotenv
import discord
from discord import app_commands
import openai
import jsonpickle
import json

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class message(object):
    def __init__(self, author, content):
        self.role = author
        self.content = content

class chat(object):
    def __init__(self):
        self.tokenCost = 0
        self.messages = []
        self.lastMessage = message("", "")
    
    def __str__(self):
        return str(self.messages)
    
    def askGpt(self, input : str):
        self.messages.append(message("user", input))
        self.lastMessage = self.messages[-1]
        messageData = []
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[x.__dict__ for x in self.messages]
        )
        print(response)
        tokenUsage = "promt token : " + str(response["usage"]["prompt_tokens"]) + " , completion token : " + str(response["usage"]["completion_tokens"]) + " , total token : " + str(response["usage"]["total_tokens"])
        print(tokenUsage)
        msg = response["choices"][0]["message"]
        self.messages.append(message(msg["role"], msg["content"]))
        self.lastMessage = self.messages[-1]
        cost = round(int(response["usage"]["total_tokens"])*(0.002/1000),7)
        return self.lastMessage.content,cost

chats = dict[int,chat]()

def exportChats(chatArray):
    return jsonpickle.encode(chatArray,unpicklable=False)

def loadChats(jsonChats):
    return jsonpickle.decode(jsonChats)

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

    
@tree.command(name="clear",description="Clears the channel")
async def clear(interaction : discord.Interaction):
    await interaction.channel.purge(limit=1000000)

@tree.command(name="ask-chat",description="Asks GPT-3 a question")
async def askGPT(interaction : discord.Interaction, question : str):
    channelID = interaction.channel.id
    if channelID not in chats:
        chats[channelID] = chat()
    currentChat: chat = chats[channelID]
    await interaction.response.send_message("waiting for GPT-3 response...")
    response,cost = currentChat.askGpt(question)
    msg = await interaction.original_response()
    await msg.edit(content="you said : " + question + "\nGPT-3 said : " + response+"\n\n"+"it costed "+str(cost)+" $")

@tree.command(name="ask",description="Asks a question to the bot")
async def ask(interaction : discord.Interaction, question : str):
    await interaction.response.send_message("waiting for response...")
    tempchat = chat()
    response,cost = tempchat.askGpt(question)
    msg = await interaction.original_response()
    await msg.edit(content="you ask : " + question + "\n\n" + response+"\n\n"+"it costed "+str(cost)+" $")


@tree.command(name="rickroll",description="Rickrolls a user")
async def rickroll(interaction : discord.Interaction, user : discord.Member):
    #send a rickroll gif to the user privately
    await user.send("https://tenor.com/bEWOf.gif")
    await interaction.response.send_message(f"Rickrolled {user.name}!",ephemeral=True)




@tree.context_menu(name="greet")
async def greet(interaction : discord.Interaction, user : discord.Member):
    await interaction.response.send_message(f"Hello {user.name}!",ephemeral=True)

def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    chatGPTSecret = os.getenv("CHATGPT_SECRET")
    openai.organization = "org-caQ8goqyO6vSXZQyq8vc4tIL"
    openai.api_key = chatGPTSecret
    client.run(token)

if __name__ == "__main__":
    main()