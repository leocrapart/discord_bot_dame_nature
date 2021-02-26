import copy
from tinydb import TinyDB, Query
db = TinyDB("db.json")

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


class Warbot:
	def __init__(self, name, lvl=1, xp=0):
		self.name = name
		self.lvl = lvl
		self.xp = xp

	def copy(self, prop, new_value):
		warbot_copy = copy.copy(self)
		warbot_copy.__dict__[prop] = new_value

		return warbot_copy

def create_warbot(warbot_name):
	warbot = Warbot(warbot_name)
	warbot_dict = warbot2dict(warbot)

	if len(db.search(Query().name == warbot_name)) >= 1:
		return f"warbot {warbot_name} already exists in database"

	db.insert(warbot_dict)
	return "warbot created"

def warbot2dict(warbot):
	return {
		"name": warbot.name,
		"lvl": warbot.lvl,
		"xp": warbot.xp
	}

def get_warbot(warbot_name):
	warbot_dict = query_warbot(warbot_name)
	warbot = dict2warbot(warbot_dict)
	return warbot

def query_warbot(warbot_name):
	result = db.search(Query().name == warbot_name)
	if len(result) > 0:
		warbot_dict = result[0]
		return warbot_dict
	else:
		return null_warbot_dict()

def null_warbot():
	return Warbot("null_warbot")

def null_warbot_dict():
	a_null_warbot = null_warbot()
	return warbot2dict(a_null_warbot)

def dict2warbot(warbot_dict):
	return Warbot(warbot_dict["name"], warbot_dict["lvl"], warbot_dict["xp"])

def get_warbot_description(warbot):
	description = f"{warbot.name} warbot is level {warbot.lvl} with {warbot.xp}/{xp_threshold_to_lvl_up(warbot.lvl)} xp."
	return description

def xp_threshold_to_lvl_up(warbot_lvl):
	lvl_str = str(warbot_lvl)
	return xp_of_lvls[lvl_str]

def add_xp_to_warbot(warbot, xp_ammount):
	new_xp_count = warbot.xp + xp_ammount
	experienced_warbot = warbot.copy("xp", new_xp_count)

	if warbot_can_lvl_up(experienced_warbot):
		lvl_uped_warbot = lvl_up_warbot(experienced_warbot)
		experienced_warbot = lvl_uped_warbot
	return experienced_warbot

def warbot_can_lvl_up(warbot):
	xp_threshold = xp_threshold_to_lvl_up(warbot.lvl)
	if warbot.xp > xp_threshold :
		return True
	return False

def lvl_up_warbot(warbot):
	new_xp = warbot.xp - xp_of_lvls[str(warbot.lvl)]
	less_xp_warbot = warbot.copy("xp", new_xp)

	new_lvl = warbot.lvl + 1
	lvl_uped_warbot = less_xp_warbot.copy("lvl", new_lvl)

	return lvl_uped_warbot

def delete_warbot(warbot_name):
	db.remove(Query().name == warbot_name)

def save_warbot(warbot):
	warbot_dict = warbot2dict(warbot)
	db.update(warbot_dict, Query().name == warbot.name)


def test():
	#creation_to_deletion_scenario()

	warbot_name = "kratos"
	xp_amount = 20

	creation_msg = create_warbot(warbot_name)
	if successful_warbot_creation(creation_msg):
		warbot = get_warbot(warbot_name)
		experienced_warbot = add_xp_to_warbot(warbot, xp_amount)
		print(get_warbot_description(experienced_warbot))
		save_warbot(experienced_warbot)
	else:
		print(creation_msg)
		warbot = get_warbot(warbot_name)
		print(get_warbot_description(warbot))
	#delete_warbot(warbot_name)

def successful_warbot_creation(creation_msg):
	return creation_msg == "warbot created"

def creation_to_deletion_scenario():
	warbot_name = "kratos"
	xp_amount = 10

	creation_msg = create_warbot(warbot_name)
	if successful_warbot_creation(creation_msg): 
		warbot = get_warbot(warbot_name)
		warbot_dict = warbot2dict(warbot)
		print("warbot after creation =>", warbot_dict)

		warbot_description = get_warbot_description(warbot)
		print("warbot description =>", warbot_description)

		warbot_experienced = add_xp_to_warbot(warbot, xp_amount)
		save_warbot(warbot_experienced)
		warbot_experienced_from_db = get_warbot(warbot_name)
		print("warbot_experienced_from_db =>", get_warbot_description(warbot_experienced_from_db))

	else: 
		print(creation_msg)

	delete_warbot(warbot_name)
	warbot_after_deletion = get_warbot(warbot_name)
	print(" warbot_after_deletion =>",get_warbot_description(warbot_after_deletion))

test()