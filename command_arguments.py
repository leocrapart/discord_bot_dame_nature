import re

def get_command_and_args(text):
  command = get_command(text)
  args = get_args(text)
  return (command, args)


def get_args(text):
  command = get_command(text)
  if command:
    first_space_index = None
    try:
      first_space_index = text.index(" ")
    except:
      args = []
    
    if first_space_index:
      arg_string = text[first_space_index:]
      arg_string_striped = arg_string.strip()
      args = re.split(r"\ +", arg_string_striped)
    else:
      args = []
    return args


def get_command(text):
  command = ""
  if is_command(text):
    command = fill_command(text)
  return command


def is_command(text):
  return text.startswith("*")


def fill_command(text):
  command = ""
  if is_command_with_args(text):
    first_space_index = get_first_space_index(text)
    command = text[1:first_space_index]
  else:
    command = text[1:]
  return command


def is_command_with_args(text):
  first_space_index = 0
  try:
    first_space_index = text.index(" ")
  except:
    pass
  if first_space_index > 0:
    return True
  return False


def get_first_space_index(text):
  return text.index(" ")

