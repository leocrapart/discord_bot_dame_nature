import discord
import os
from dotenv import load_dotenv
from command_extractor import CommandExtractor
from warbot import WarbotGenerator

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


class Command:
  def __init__(self, code, args):
    self.code = code
    self.args = args

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = Reader(message.content).command()
    sender = Sender(message)
    await command.process(sender)


class Reader:
  def __init__(self, text):
    self.text = text
  
  def command(self):
    code, args = CommandExtractor().extract_command(self.text)
    return CommandFactory().command_for(code, args)


class CommandFactory:
  COMMANDS = {
    "hello": "HelloCommand",
    "show-warbots": "ShowWarbotsCommand",
    "generate-warbots": "GenerateWarbotsCommand", 
    "kill-warbots": "KillWarbotsCommand", 
    "free-my-bot": "FreeBotCommand",
    "create-bot": "CreateBotCommand",
    "stats": "StatsCommand",
    "add-xp": "AddXpCommand",
    "add-attack": "AddAttackCommand",
    "add-health": "AddHealthCommand"
  }

  def command_for(self, code, args=[]):
    try:
      return eval(self.COMMANDS[code])(args)
    except:
      return NullCommand()

class Sender:
  def __init__(self, message):
    self.message = message
  
  async def send_hello(self):
    await self.message.channel.send("Hello from speaker")

  async def send(self, text):
    await self.message.channel.send(text)


class NullCommand:
  def __init__(self):
    self.args = []

  async def process(self, sender):
    #await sender.send("not a command")
    pass

class HelloCommand:
  def __init__(self, args):
    self.args = args

  async def process(self, sender):
    await sender.send(self.success_message())
  
  def success_message(self):
    return "Hello !"

class GenerateWarbotsCommand:
  def __init__(self, args):
    self.args = args
  
  async def process(self, sender):
    number_of_args = len(self.args)
    if number_of_args >= 2:
      difficulty = self.args[0]
      amount = int(self.args[1])
      warbots = WarbotGenerator().generate_random_warbots(difficulty, amount)
      response = f" Here are your {amount} {difficulty} warbots !"
      for warbot in warbots:
        response += f"\n {warbot.presentation()}"
      await sender.send(response)
    elif number_of_args < 2:
      await sender.send(self.error_message())

  def error_message(self):
    return "I need a difficulty (easy, medium, hard) and a number to produce these warbots."

class ShowWarbotsCommand:
  def __init__(self, args):
    self.args = args
  
  async def process(self, sender):
    await sender.send(self.success_message())
  
  def success_message(self):
    return "showing warbots ..."


class KillWarbotsCommand:
  def __init__(self, args):
    self.args = args
  
  async def process(self, sender):
    await sender.send(self.success_message())

  
  def success_message(self):
    return "Warbots deleted"


class CreateBotCommand:
  def __init__(self, args):
    self.args = args

  async def process(self, sender):
    if len(self.args) > 0:
      await sender.send(self.success_message())
    else:
      await sender.send(self.error_message())
  
  def success_message(self):
    return "Your bot have been created"

  def error_message(self):
    return "I need a name to create your bot"


class FreeBotCommand:
  def __init__(self, args):
    self.args = args
  
  async def process(self, sender):
    await sender.send(self.success_message())
  
  def success_message(self):
    return "#playerbot_name has been freed, he's now free to do what he wants in the real of nature and i'll use him carefully"

class StatsCommand:
  def __init__(self, args):
    self.args = args

  async def process(self, sender):
    if len(self.args) > 0:
      await sender.send(f"stats of {self.args[0]}")
    else:
      await sender.send("Your stats")

class AddAttackCommand:
  def __init__(self, args):
    self.args = args
  
  async def process(self, sender):
    number_of_args = len(self.args)
    if number_of_args > 1:
      await sender.send(self.success_message())
    elif number_of_args <= 1:
      await sender.send(self.error_message())
  
  def success_message(self):
    return f"{self.args[1]} attack added to {self.args[0]} "
  
  def error_message(self):
    return "I need a name and a value to execute this"
  

class AddXpCommand:
  def __init__(self, args):
    self.args = args
  
  async def process(self, sender):
    number_of_args = len(self.args)
    if number_of_args > 1:
      await sender.send(self.success_message())
    elif number_of_args <= 1:
      await sender.send(self.error_message())

  def success_message(self):
    return f"{self.args[1]} xp added to {self.args[0]} "
  
  def error_message(self):
    return "I need a name and a value to execute this"


class AddHealthCommand:
  def __init__(self, args):
    self.args = args

  async def process(self, sender):
    number_of_args = len(self.args)
    if number_of_args > 1:
      await sender.send(self.success_message())
    elif number_of_args <= 1:
      await sender.send(self.error_message())


  def success_message(self):
    return f"{self.args[1]} health added to {self.args[0]} "
  
  def error_message(self):
    return "I need a name and a value to execute this"



load_dotenv()
client.run(os.getenv("TOKEN"))