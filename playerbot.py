from tinydb import TinyDB, Query

class PlayerBot:
    xp_of_lvls = {
        "1": 10,
        "2": 20,
        "3": 40,
        "4": 80,
        "5": 160,
        "6": 320,
        "7": 640,
        "8": 1280,
        "9": 2560
        }
    def __init__(self, name, lvl=1, xp=0):
        self.name = name
        self.lvl = lvl
        self.xp = xp

    def description(self):
        return f"{self.name} is level {self.lvl} with {self.xp}/{self.xp_threshold()} xp."
        
    def xp_threshold(self):
      lvl_str = str(self.lvl)
      return self.xp_of_lvls[lvl_str]

    def add_xp(self, xp_amount):
        xp_to_give = xp_amount
        while self.can_receive_xp(xp_to_give):
          remaining_xp = self.receive_xp(xp_to_give)
          xp_to_give = remaining_xp

    def can_receive_xp(self, xp_amount):
      if xp_amount == 0:
        return False
      if self.is_not_lvl_max():
        return True
      elif self.xp < self.xp_threshold():
        return True
      else:
        return False 
      
    def receive_xp(self, xp_amount):
      if self.giving_xp_will_lvl_up(xp_amount):
        remaining_xp = self.calculate_remaining_xp_to_give(xp_amount)
        self.set_xp_to_threshold()
        if self.is_not_lvl_max():
          self.lvl_up()
      else:
        self.give_xp(xp_amount)
        remaining_xp = 0
      return remaining_xp
    
    def required_xp_to_lvl_up(self):
      return self.xp_threshold() - self.xp

    def giving_xp_will_lvl_up(self, xp_amount):
      return xp_amount >= self.required_xp_to_lvl_up()
    
    def calculate_remaining_xp_to_give(self, xp_to_give):
        return xp_to_give - self.required_xp_to_lvl_up()
    
    def set_xp_to_threshold(self):
      self.xp = self.xp_threshold()

    def give_xp(self, xp_amount):
      self.xp += xp_amount

    def save(self):
        Db().save_playerbot(self)

    def is_not_lvl_max(self):
      if self.lvl < self.max_lvl_possible():
          return True
      else:
          return False

    def max_lvl_possible(self):
        return len(self.xp_of_lvls)

    def next_lvl_str(self):
        next_lvl = self.lvl + 1
        return str(next_lvl)

    def lvl_up(self):
        self.decrease_xp()
        self.lvl += 1
        #self.print_lvl_up_message()

    def decrease_xp(self):
        self.xp -= self.xp_threshold()

    def print_lvl_up_message(self):
        print(f"{self.name} is now level {self.lvl}!")


class Db:
    db = TinyDB("db.json")
    def save_playerbot(self, playerbot):
        playerbot_dict = self.playerbot_to_dict(playerbot)
        if self.playerbot_already_exists(playerbot.name):
            self.update_playerbot_record(playerbot_dict)
        else:
            self.create_new_playerbot_record(playerbot_dict)

    def playerbot_to_dict(self, playerbot):
        return {
            "name": playerbot.name,
            "lvl": playerbot.lvl,
            "xp": playerbot.xp
        }

    def playerbot_already_exists(self, playerbot_name):
        query_result = self.query_playerbot(playerbot_name)
        playerbot_number = len(query_result)
        return playerbot_number > 0

    def query_playerbot(self, playerbot_name):
        return self.db.search(Query().name == playerbot_name)

    def update_playerbot_record(self, playerbot_dict):
        self.db.update(playerbot_dict, Query().name == playerbot_dict["name"])

    def create_new_playerbot_record(self, playerbot_dict):
        self.db.insert(playerbot_dict)

    def get_playerbot(self, playerbot_name):
        playerbot_dict = self.get_playerbot_dict_from_db(playerbot_name)
        player = self.dict2playerbot(playerbot_dict)
        return player

    def get_playerbot_dict_from_db(self, playerbot_name):
        return self.db.search(Query().name == playerbot_name)[0]

    def dict2playerbot(self, p_dict):
        return PlayerBot(p_dict["name"], p_dict["lvl"], p_dict["xp"])


class PlayerBotTest:
  def description_scenario(self):
    playerbot = self.create_kratos()
    description = playerbot.description()
    expected_desc = "kratos is level 1 with 0/10 xp."
    assert description == expected_desc, "description_scenario"
  
  def create_kratos(self):
    playerbot_name = "kratos"
    return PlayerBot(playerbot_name)

  def print_test_result(self, test_name, test_content):
    print(f"# {test_name} test #")
    print(test_content)
    print("#                        #")
    print(" ")

  def add_xp_scenario(self):
    playerbot = self.create_kratos()
    xp = 500
    playerbot.add_xp(xp)
    description = playerbot.description()
    expected_desc = "kratos is level 6 with 190/320 xp."
    assert description == expected_desc, "add_xp_scenario"
  
  def save_scenario(self):
    playerbot = self.create_kratos()
    playerbot.save()
    playerbot_from_db = Db().get_playerbot(playerbot.name)
    playerbot_from_db_desc = playerbot_from_db.description()
    expected_desc = "kratos is level 1 with 0/10 xp."
    assert playerbot_from_db_desc == expected_desc, "save_scenario"

  def xp_and_save_scenario(self):
    playerbot = self.create_kratos()
    xp = 500
    playerbot.add_xp(xp)
    playerbot.save()
    expected_desc = "kratos is level 6 with 190/320 xp."
    #print(playerbot.description())
    assert playerbot.description() == expected_desc, "xp_and_save_scenario"

  def max_lvl_scenario(self):
    playerbot = self.create_kratos()
    too_much_xp = 50000
    playerbot.add_xp(too_much_xp)
    desc = playerbot.description()

    max_lvl_possible = playerbot.max_lvl_possible()
    max_lvl_xp = self.get_max_xp(playerbot)

    expected_desc = f"kratos is level {max_lvl_possible} with {max_lvl_xp}/{max_lvl_xp} xp."
    assert desc == expected_desc, "max_lvl_scenario"

  def get_max_xp(self, playerbot):
    max_lvl_possible = playerbot.max_lvl_possible()
    return playerbot.xp_of_lvls[str(max_lvl_possible)]

  def tests_green(self):
    print("Playerbot test OK")




test = PlayerBotTest()
test.description_scenario()
test.add_xp_scenario()
test.save_scenario()
test.xp_and_save_scenario()
test.max_lvl_scenario()
test.tests_green()