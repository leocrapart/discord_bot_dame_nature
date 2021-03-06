import re



class CommandExtractor:
  def extract_command(self, message):
    return self.get_code_and_args(message)


  def get_code_and_args(self, text):
    code = self.get_code(text)
    args = self.get_args(text)
    return (code, args)

  def get_args(self, text):
    code = self.get_code(text)
    if code:
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


  def get_code(self, text):
    code = ""
    if self.is_command(text):
      code = self.fill_code(text)
    return code


  def is_command(self, text):
    return text.startswith("*")


  def fill_code(self, text):
    code = ""
    if self.is_command_with_args(text):
      first_space_index = self.get_first_space_index(text)
      code = text[1:first_space_index]
    else:
      code = text[1:]
    return code


  def is_command_with_args(self, text):
    first_space_index = 0
    try:
      first_space_index = text.index(" ")
    except:
      pass
    if first_space_index > 0:
      return True
    return False


  def get_first_space_index(self, text):
    return text.index(" ")

