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
    #command printing debug
    print(command.name)
    print(command.args)
    discord_listener = DiscordListener(command)
    discord_speaker = DiscordSpeaker(message)

    #hello command
    if discord_listener.is_command("hello"):
      await discord_speaker.say_hello()

    #stats command
    if discord_listener.is_command("stats"):
      command = discord_listener.command
      number_of_args = len(command.args)
      if number_of_args > 0:
        await discord_speaker.say(f"stats of {command.args[0]}")
      else:
        await discord_speaker.say("Your stats")

    #create bot command    
    if discord_listener.is_command("create-bot"):
      command = discord_listener.command
      number_of_args = len(command.args)
      if number_of_args > 0:
        await discord_speaker.say(f"We are creating {command.args[0]} from dust, wait a minute...")
      else:
        await discord_speaker.say("I need a name to create your bot")

    #free my bot command    
    if discord_listener.is_command("free-my-bot"):
      await discord_speaker.say("#playerbot_name has been freed, he's now free to do what he wants in the real of nature and i'll use him carefully")

    #add xp command
    if discord_listener.is_command("add-xp"):
      command = discord_listener.command
      number_of_args = len(command.args)
      if number_of_args > 1:
        await discord_speaker.say(f"{command.args[1]} xp added to {command.args[0]} ")
      elif number_of_args <= 1:
        await discord_speaker.say("I need a name and a value to execute this")
    
    #add health command
    if discord_listener.is_command("add-health"):
      command = discord_listener.command
      number_of_args = len(command.args)
      if number_of_args > 1:
        await discord_speaker.say(f"{command.args[1]} health added to {command.args[0]} ")
      elif number_of_args <= 1:
        await discord_speaker.say("I need a name and a value to execute this")

    #add attack command
    if discord_listener.is_command("add-attack"):
      command = discord_listener.command
      number_of_args = len(command.args)
      if number_of_args > 1:
        await discord_speaker.say(f"{command.args[1]} attack added to {command.args[0]} ")
      elif number_of_args <= 1:
        await discord_speaker.say("I need a name and a value to execute this")
      
def message2command(message):
    message_text = message.content
    command_tuple = command_arguments.get_command_and_args(message_text)
    command_name, command_args = command_tuple
    return Command(command_name, command_args)

#listens to commands so that it can tell you what command to react to
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

  async def say(self, text):
    await self.message.channel.send(text)


load_dotenv()
client.run(os.getenv("TOKEN"))