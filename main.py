import discord
import os
from dotenv import load_dotenv
import command_arguments

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = message2command(message)
    discord_listener = DiscordListener(command)
    discord_speaker = DiscordSpeaker(message)

    if discord_listener.is_command("hello"):
      await discord_speaker.say_hello()

def message2command(message):
    message_text = message.content
    command_tuple = command_arguments.get_command_and_args(message_text)
    command_name, command_args = command_tuple
    return Command(command_name, command_args)

#I listen to commands so that i can tell you what command to react to
class DiscordListener:
    command_prefix = "*"
    def __init__(self, command):
        self.command = command
    
    def is_command(self, command_name):
      return self.command_name().startswith(command_name)

    def command_name(self):
      return self.command.name

#I am a command with a name and args
class Command:
  def __init__(self, name, args):
    self.name = name
    self.args = args

#I send messages on the discord channel
class DiscordSpeaker:
  def __init__(self, message):
    self.message = message
  
  async def say_hello(self):
    await self.message.channel.send("Hello from speaker")


load_dotenv()
client.run(os.getenv("TOKEN"))