from collections import defaultdict
import random


class Land:
    def __init__(self, column=0, line=0, is_claimed=False, is_mowed=False, is_wet=False, seed=''):
        self.isClaimed = is_claimed
        self.isMowed = is_mowed
        self.isWet = is_wet
        self.seed = [seed, 0, 0]
        self.cords = [column, line]
        self.wet = 0

    def claim(self, is_claimed=True):
        self.isClaimed = is_claimed

    def mow(self, is_mowed=True):
        if self.isClaimed:
            self.isMowed = is_mowed

    def water(self, is_wet=True):
        if self.isClaimed:
            if self.isWet != is_wet:
                self.isWet = is_wet
                self.wet = 0
                if is_wet:
                    self.wet = random.randrange(1500, 4000)
                return is_wet
        return False

    def plant(self, seed, state=0, age=1):
        if self.isMowed:
            self.seed = [seed, state, age]
            return True
        else:
            return False

    def grow(self, growth=1):
        seed = self.seed[0]
        state = self.seed[1]
        age = self.seed[2]

        if seed != '':
            if self.isWet:
                growth *= 1.5

            if age == my_game.max_age:
                return

            if not age + 1 > my_game.max_age:
                state += growth
                if state >= random.randrange(500, 1000):
                    age += 1
                    state = 0

            self.seed = [seed, state, age]

    def info(self):
        print(f'''
                Info:
                >> Claimed: {self.isClaimed}
                >> Mowed: {self.isMowed}
                >> Watered: {self.isWet}
                >> Seed: {self.seed}
                ''')


class Game(object):
    max_age = 4

    def __init__(self, gc, gl):
        self.column = gc
        self.line = gl

        self.lands = [[Land(column=i, line=j) for i in range(gc)] for j in range(gl)]
        self.land(1, 1).claim()
        self.inventory_dict = defaultdict(int)

    def add(self, item, amount=1):
        item = str(f"{item[:1].upper()}{item[1:].lower()}")
        self.inventory_dict[item] += amount

    def plant(self, c, l, seed):
        if self.inventory_dict[seed] > 0:
            if my_game.land(c, l).plant(seed):
                self.inventory_dict[seed] -= 1
                return True
            else:
                return False

    def land(self, c, l):
        return self.lands[c][l]

    def cords(self):
        return self.column, self.line

    def inventory(self, item):
        return self.inventory_dict[f"{item[:1].upper()}{item[1:].lower()}"]


my_game = Game(3, 3)