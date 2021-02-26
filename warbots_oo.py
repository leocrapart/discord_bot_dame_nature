from tinydb import TinyDB, Query


class Warbot:

    xp_of_lvls = {
        "1": 15,
        "2": 25,
        "3": 40,
        "4": 55,
        "5": 80,
        "6": 100,
        "7": 130,
        "8": 160,
        "9": 200
        }

    def __init__(self, name, xp=0, lvl=1):
        self.name = name
        self.xp = xp
        self.lvl = lvl
    
    def to_dict(self):
        return {
            "name": self.name,
            "xp": self.xp,
            "lvl": self.lvl
            }
    
    def add_xp(self, xp_amount):
        self.xp += xp_amount
        while self.enought_xp_to_lvl_up():
            self.lvl_up()

    def enought_xp_to_lvl_up(self):
        return self.xp > self.xp_threshold_to_lvl_up()

    def xp_threshold_to_lvl_up(self):
        lvl_str = str(self.lvl)
        return self.xp_of_lvls[lvl_str]

    def lvl_up(self):
        self.xp -= self.xp_threshold_to_lvl_up()
        self.lvl += 1
        self.print_lvl_up_message()
        
    def print_lvl_up_message(self):
        print(f"{self.name} warbot reached lvl {self.lvl}! ")

    def print_stats(self):
        print(f"{self.name} warbot is level {self.lvl} with {self.xp}/{self.xp_threshold_to_lvl_up()} xp.")

    def save(self):
        warbot_dict = self.to_dict()
        db.update(warbot_dict, Query().name == self.name)


class WarbotHelper:
    db = TinyDB("db.json")

    def get_warbot(self, warbot_name):
        warbot_dict = db.search(Query().name == warbot_name)[0]
        warbot = self.warbot_dict_to_object(warbot_dict)
        return warbot

    def warbot_dict_to_object(self, warbot_dict):
        warbot = Warbot(warbot_dict["name"], warbot_dict["xp"], warbot_dict["lvl"])
        return warbot


db = TinyDB("db.json")
helper = WarbotHelper()

def create_new_warbot(warbot_name):
    new_warbot = Warbot(warbot_name)
    warbot_dict = new_warbot.to_dict()
    db.insert(warbot_dict)

def add_xp_to_warbot(warbot_name, xp_amount):
    warbot = helper.get_warbot(warbot_name)
    warbot.add_xp(xp_amount)
    warbot.save()

def get_warbot_xp(warbot_name):
    warbot = helper.get_warbot(warbot_name)
    return warbot.xp

def get_warbot_lvl(warbot_name):
    warbot = helper.get_warbot(warbot_name)
    return warbot.lvl


create_new_warbot("enbot")
create_new_warbot("kratos")

enbot_lvl = get_warbot_lvl("enbot")
kratos_xp = get_warbot_xp("kratos")


add_xp_to_warbot("kratos", 100)
add_xp_to_warbot("enbot", 200)

kratos = helper.get_warbot("kratos")
kratos.print_stats()