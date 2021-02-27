from tinydb import TinyDB, Query

class Warbot:
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

    def add_xp(self, xp_amount):
        self.xp += xp_amount
        while self.can_lvl_up():
            self.lvl_up()
    
    def save(self):
        Db().save_warbot(self)

    ##private
    def xp_threshold(self):
        lvl_str = str(self.lvl)
        return self.xp_of_lvls[lvl_str]

    def can_lvl_up(self):
        return self.has_enought_xp() and self.is_not_lvl_max()

    def has_enought_xp(self):
        return self.xp > self.xp_threshold()

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
        self.print_lvl_up_message()

    def decrease_xp(self):
        self.xp -= self.xp_threshold()

    def print_lvl_up_message(self):
        print(f"{self.name} is now level {self.lvl}!")


class Db:
    db = TinyDB("db.json")
    def save_warbot(self, warbot):
        warbot_dict = self.warbot_to_dict(warbot)
        if self.warbot_already_exists(warbot.name):
            self.update_warbot_record(warbot_dict)
        else:
            self.create_new_warbot_record(warbot_dict)

    def warbot_to_dict(self, warbot):
        return {
            "name": warbot.name,
            "lvl": warbot.lvl,
            "xp": warbot.xp
        }

    def warbot_already_exists(self, warbot_name):
        query_result = self.query_warbot(warbot_name)
        warbot_number = len(query_result)
        return warbot_number > 0

    def query_warbot(self, warbot_name):
        return self.db.search(Query().name == warbot_name)

    def update_warbot_record(self, warbot_dict):
        self.db.update(warbot_dict, Query().name == warbot_dict["name"])

    def create_new_warbot_record(self, warbot_dict):
        self.db.insert(warbot_dict)

    def get_warbot(self, warbot_name):
        warbot_dict = self.get_warbot_dict_from_db(warbot_name)
        warbot = self.dict2warbot(warbot_dict)
        return warbot

    def get_warbot_dict_from_db(self, warbot_name):
        return self.db.search(Query().name == warbot_name)[0]

    def dict2warbot(self, w_dict):
        return Warbot(w_dict["name"], w_dict["lvl"], w_dict["xp"])


class WarbotTest:
    def description_scenario(self):
        warbot = self.create_kratos()
        description = warbot.description()
        self.print_test_result("description", description)


    def print_test_result(self, test_name, test_content):
        print(f"# {test_name} test #")
        print(test_content)
        print("#                        #")
        print(" ")

    def add_xp_scenario(self):
        warbot = self.create_kratos()
        xp = 500
        warbot.add_xp(xp)
        description = warbot.description()
        self.print_test_result("xp", description)

    def save_scenario(self):
        warbot = self.create_kratos()
        warbot.save()
        warbot_from_db = Db().get_warbot(warbot.name)
        warbot_from_db_desc = warbot_from_db.description()
        self.print_test_result("warbot from db", warbot_from_db_desc)

    def xp_and_save_scenario(self):
        warbot = self.create_kratos()
        xp = 500
        warbot.add_xp(xp)
        warbot.save()
        self.print_test_result("xp and save", warbot.description())

    def max_lvl_scenario(self):
        warbot = self.create_kratos()
        too_much_xp = 50000
        warbot.add_xp(too_much_xp)
        desc = warbot.description()
        self.print_test_result("max lvl", desc)


    def create_kratos(self):
        warbot_name = "kratos"
        return Warbot(warbot_name)


test = WarbotTest()
test.description_scenario()
test.add_xp_scenario()
test.save_scenario()
test.xp_and_save_scenario()
test.max_lvl_scenario()