import discord
import os
from dotenv import load_dotenv
import warbots
import command_arguments

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    discord_listener = DiscordListener(message)
    
    command_prefix = "*"
    print("### debug")
    print(message.author)
    print(client.user)




    message_text = message.content
    if message_text.startswith("*"):
        command, args = command_arguments.get_command_and_args(message_text)
        await message.channel.send(command)
        await message.channel.send(args)

    if message_text.startswith("*hello dame nature"):
        await message.channel.send("Bienvenue dans les regles du jeu, je suis dame nature.")

    if message_text.startswith("*create new warbot leebot"):
        warbots.create_new_warbot("leebot")
        await message.channel.send("New warbot created")

class DiscordListener:
    command_prefix = "*"
    def __init__(self, message):
        self.message = message



load_dotenv()
client.run(os.getenv("TOKEN"))