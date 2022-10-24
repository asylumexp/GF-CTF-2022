from GameFrame import RedBot, Globals
import random
from enum import Enum

class STATE(Enum):
    CHILL = 1
    STRIKE = 2
    FLAGRETURN = 3

class Red1(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state=STATE.FLAGRETURN


    def tick(self):
        print(self.curr_state)
        if self.curr_state == STATE.FLAGRETURN:
            self.flagreturn()
        if self.curr_state == STATE.CHILL:
            self.wait()
        # if self.curr_state == STATE.STRIKE:
        #     self.STRIKE()

    def flagreturn(self):
        if self.point_to_point_distance(self.x, self.y, Globals.blue_flag.x, Globals.blue_flag.y)>20:
            self.turn_towards(Globals.blue_flag.x,Globals.blue_flag.y)
            self.drive_forward(Globals.SLOW)
        else:
            self.curr_state= STATE.CHILL

    def wait(self):
        bot, distance = self.closest_enemy_to_flag()
        self.turn_towards(bot.x, bot.y, Globals.FAST)

    # def STRIKE(self):

    def closest_enemy_to_flag(self):
        closest_bot = Globals.red_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         Globals.blue_flag.x, Globals.blue_flag.y)
        for curr_bot in Globals.red_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         Globals.blue_flag.x, Globals.blue_flag.y)
            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance
