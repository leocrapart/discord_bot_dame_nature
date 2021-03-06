import random

class WarbotGenerator:
    def generate_random_warbots(self, difficulty, amount):
        lvl_range = self.lvl_ranges(difficulty)
        empty_warbots = [lvl_range for i in range(amount)]
        random_warbots = list(map(self.random_warbot_from_lvl_range, empty_warbots))
        return random_warbots

    def random_warbot_from_lvl_range(self, lvl_range):
        random_lvl = self.random_between(lvl_range)
        random_warbot = self.create_random_warbot(random_lvl)
        return random_warbot
    
    def stat_range(self, lvl):
        return {
            "health": HealthInterval().interval(lvl),
            "attack": AttackInterval().interval(lvl)
        }

    def lvl_ranges(self, difficulty):
        lvl_ranges = DifficultySystem().lvl_range(difficulty)
        return lvl_ranges

    def create_random_warbot(self, lvl):
        stat_range = self.stat_range(lvl)
        attack_range = stat_range["attack"]
        health_range = stat_range["health"]
        random_attack = self.random_between(attack_range)
        random_health = self.random_between(health_range)
        random_warbot = Warbot(random_health, random_attack, lvl)
        return random_warbot

    def random_between(self, range):
        return random.randrange(range[0], range[1] +1)


class Warbot:
    def __init__(self, lvl, health, attack):
        self.lvl = lvl
        self.attack = attack
        self.health = health
    
    def use_stat(self):
        return stat.range()

    def present_yourself(self):
        print(f"I am lvl {self.lvl} with {self.health} health and {self.attack} attack.")
    
    def presentation(self):
        presentation = f"I am lvl {self.lvl} with {self.health} health and {self.attack} attack."
        return presentation




class HealthInterval:
    health_ranges = {
        "1": [2, 4],
        "2": [3, 5],
        "3": [4, 7],
        "4": [5, 9],
        "5": [7, 10],
        "6": [8, 11],
        "7": [9, 12],
        "8": [10, 13],
        "9": [11, 14],
        "10": [12, 15]
    }
    def interval(self, lvl):
        return self.health_ranges[str(lvl)]

class AttackInterval:
    attack_ranges = {
        "1": [1, 2],
        "2": [2, 3],
        "3": [3, 4],
        "4": [4, 5],
        "5": [5, 6],
        "6": [6, 7],
        "7": [7, 8],
        "8": [8, 9],
        "9": [9, 10],
        "10": [10, 11]
    }
    def interval(self, lvl):
        return self.attack_ranges[str(lvl)]


class DifficultySystem:
    lvl_ranges = {
        "easy": [1, 3],
        "medium": [4, 6],
        "hard": [7, 10]
    }

    def lvl_range(self, difficulty):
        return self.lvl_ranges[str(difficulty)]


class RandomStatGenerator:
    def generate_stat(self):
        return


class DefaultStatGenerator:
    def generate_stat(self):
        return

## test zone
def print_warbots():
    warbot_generator = WarbotGenerator()
    random_warbots = warbot_generator.generate_random_warbots("hard", 2)
    for warbot in random_warbots:
        warbot.present_yourself()
#print_warbots()

def test_warbot_difficulties():
    assert is_difficulty_correct("easy")
    assert is_difficulty_correct("medium")
    assert is_difficulty_correct("hard")

def is_difficulty_correct(difficulty):
    good_difficulty_warbot = warbot_of_difficulty(difficulty)
    return is_good_difficulty_warbot(good_difficulty_warbot, difficulty)

def warbot_of_difficulty(difficulty):
    difficulty_test_args = {
        "easy": [3, 7, 4],
        "medium": [4, 8, 5],
        "hard": [7, 9, 7]
    }
    args = difficulty_test_args[difficulty]
    return Warbot(args[0], args[1], args[2])

def is_good_difficulty_warbot(warbot, difficulty):
    assert is_good_difficulty_lvl(warbot, difficulty)
    assert has_coresponding_attack(warbot)
    assert has_corresponding_health(warbot)
    return True

def is_good_difficulty_lvl(warbot, difficulty):
    lvl_interval = {
        "easy": [1, 3],
        "medium": [4, 6],
        "hard": [7, 10]
    }
    return is_into(warbot.lvl, lvl_interval[difficulty])

def is_into(number, interval):
    return number >= interval[0] and number <= interval[1]

def has_coresponding_attack(warbot):
    good_interval = AttackInterval().interval(warbot.lvl)
    return is_into(warbot.attack, good_interval)

def has_corresponding_health(warbot):
    good_interval = HealthInterval().interval(warbot.lvl)
    return is_into(warbot.health, good_interval)


test_warbot_difficulties()













def are_same_warbots(warbot1, warbot2):
    for attr in warbot1.__dict__:
        if warbot1.__dict__[attr] != warbot2.__dict__[attr]:
            return False
    return True
