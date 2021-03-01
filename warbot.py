import random

class WarbotCreator:
    intervals = [{}, {}, {}]
    def create_random_warbots(self, difficulty, amount_of_warbots):
        lvl_range = self.lvl_ranges(difficulty)
        empty_warbots = [lvl_range for i in range(amount_of_warbots)]
        random_warbots = list(map(self.random_warbot_from_lvl_range, empty_warbots))
        return random_warbots

    def random_warbot_from_lvl_range(self, lvl_range):
        random_lvl = self.random_between(lvl_range)
        random_warbot = self.create_random_warbot(random_lvl)
        return random_warbot
    
    def stat_range(self, lvl):
        return {
            "health": WarbotHealth().range(lvl),
            "attack": WarbotAttack().range(lvl)
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
    def __init__(self, health, attack, lvl):
        self.health = health
        self.attack = attack
        self.lvl = lvl

    def present_yourself(self):
        print(f"I am lvl {self.lvl} with {self.health} health and {self.attack} attack.")


class WarbotHealth:
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
    def range(self, lvl):
        return self.health_ranges[str(lvl)]

class WarbotAttack:
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
    def range(self, lvl):
        return self.attack_ranges[str(lvl)]


class DifficultySystem:
    lvl_ranges = {
        "easy": [1, 3],
        "medium": [3, 6],
        "hard": [6, 10]
    }

    def lvl_range(self, difficulty):
        return self.lvl_ranges[str(difficulty)]



warbot_creator = WarbotCreator()
random_warbots = warbot_creator.create_random_warbots("hard", 5)

for warbot in random_warbots:
    warbot.present_yourself()