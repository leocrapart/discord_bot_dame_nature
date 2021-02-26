import copy 
from tinydb import TinyDB, Query


db = TinyDB("db.json")


class Warbot:
	def __init__(self, name, lvl=1, xp=0):
		self.name = name
		self.lvl = lvl
		self.xp = xp

	def get_description(self):
		return f"Warbot {self.name} is lvl {self.lvl} with {self.xp}/{self.xp_threshold_to_lvl_up()} xp. "

	def add_xp(self, xp_amount):
		new_xp = self.xp + xp_amount
		experienced_warbot = self.copy("xp", new_xp)
		while experienced_warbot.can_lvl_up():
			lvled_up_warbot = experienced_warbot.lvl_up()
			experienced_warbot = lvled_up_warbot
			lvl_up_msg = experienced_warbot.lvl_up_message()
			print(lvl_up_msg)
		return experienced_warbot

	def save(self):
		warbot_dict = self.to_dict()
		if self.is_in_db():
			db.update(warbot_dict, Query().name == self.name)
		else:
			db.insert(warbot_dict)

	def delete(self):
		db.remove(Query().name == self.name)

    ## private
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

	def xp_threshold_to_lvl_up(self):
		lvl_str = str(self.lvl)
		xp_threshold = self.xp_of_lvls[lvl_str]
		return xp_threshold

	def is_in_db(self):
		result = db.search(Query().name == self.name)
		number_of_warbots_queried = len(result)
		return number_of_warbots_queried > 0

	def to_dict(self):
		return {
			"name": self.name,
			"lvl": self.lvl,
			"xp": self.xp
		}

	def copy(self, prop, new_value):
		warbot_copy = copy.copy(self)
		warbot_copy.__dict__[prop] = new_value
		return warbot_copy

	def can_lvl_up(self):
		xp_threshold = self.xp_threshold_to_lvl_up()
		return self.xp >= xp_threshold

	def lvl_up(self):
		xp_amount_to_decrease = self.xp_threshold_to_lvl_up()
		less_xp_warbot = self.decrease_xp(xp_amount_to_decrease)
		lvled_up_warbot = less_xp_warbot.add_one_lvl()
		return lvled_up_warbot

	def decrease_xp(self, xp_amount):
		return self.copy("xp", self.xp - xp_amount)

	def add_one_lvl(self):
		return self.copy("lvl", self.lvl +1)

	def lvl_up_message(self):
		return f"Warbot {self.name} is now level {self.lvl}! "


class NullWarbot(Warbot):
	def __init__(self):
		self.name = "Null warbot"
		self.lvl = 1
		self.xp = 0

class WarbotHelper:
	def get_warbot(warbot_name):
		if warbot_is_in_db(warbot_name):
			warbot_dict = query_warbot(warbot_name)[0]
			warbot = dict2warbot(warbot_dict)
			return warbot
		else:
			return NullWarbot()

	def dict2warbot(warbot_dict):
		return Warbot(warbot_dict["name"], warbot_dict["lvl"], warbot_dict["xp"])

	##private
	def warbot_is_in_db(warbot_name):
		number_of_warbots_queried = len(query_warbot(warbot_name))
		return number_of_warbots_queried > 0

	def query_warbot(warbot_name):
		return db.search(Query().name == warbot_name)



def test():
	warbot_class_test()
	save_test()
	add_xp_test()
	delete_test()

def warbot_class_test():
	warbot = Warbot("kratos")
	description = warbot.get_description()
	print("warbot class test =>", description)

def save_test():
	warbot_name = "kratos"
	warbot = Warbot(warbot_name)
	warbot.save()
	saved_warbot = get_warbot(warbot_name)
	description = saved_warbot.get_description()
	print("save test =>", description)

def add_xp_test():
	warbot_name = "kratos"
	xp_amount = 200
	warbot = Warbot(warbot_name)
	experienced_warbot = warbot.add_xp(xp_amount)
	description = experienced_warbot.get_description()
	print("add xp test =>", description)

def delete_test():
	warbot_name = "kratos"
	warbot = Warbot(warbot_name)
	warbot.save()

	warbot_from_db = get_warbot(warbot_name)
	description = warbot_from_db.get_description()
	print("delete test, warbot created =>", description)
	warbot.delete()

	warbot_from_db_after_deletion = get_warbot(warbot_name)
	description = warbot_from_db_after_deletion.get_description()
	print("delete test, warbot after deletion =>", description)

test()