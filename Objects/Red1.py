from GameFrame import RedBot, Globals
import random
from enum import Enum

#TEST

class STATE(Enum):
    CHILL = 1
    STRIKE = 2
    FLAGRETURN = 3
    TURNTOFLAG = 4

class Red1(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state=STATE.FLAGRETURN
        self.attacking = {
            "attacking1": [False, None],
            "attacking2": [False, None],
            "attacking3": [False, None],
            "attacking4": [False, None],
            "attacking5": [False, None]
        }

    def tick(self):
        if self.curr_state == STATE.FLAGRETURN:
            self.flagreturn()
        if self.curr_state == STATE.CHILL:
            self.wait()
        if self.curr_state == STATE.STRIKE:
             self.STRIKE()
        if self.curr_state == STATE.TURNTOFLAG:
            self.turntoflag()

    def flagreturn(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance<350:
            self.curr_state=STATE.STRIKE
        elif self.point_to_point_distance(self.x, self.y, Globals.blue_flag.x, Globals.blue_flag.y)>50:
            self.turn_towards(Globals.blue_flag.x,Globals.blue_flag.y,Globals.FAST)
            self.drive_forward(Globals.MEDIUM)
        else:
            self.curr_state= STATE.CHILL

    def wait(self):
        bot, distance = self.closest_enemy_to_flag()
        self.turn_towards(bot.x, bot.y, Globals.FAST)
        if distance<150:
            self.curr_state=STATE.STRIKE

    def STRIKE(self):
        bot, distance = self.closest_enemy_to_flag()
        angle = int(self.get_rotation_to_coordinate(bot.x,bot.y))
        self.turn_towards(bot.x, bot.y, Globals.FAST)
        if distance<100 and abs(angle-self.angle%360)<50:
                self.drive_forward(Globals.FAST)
        if distance>200:
            self.curr_state=STATE.FLAGRETURN

    def turntoflag(self):
        pass

    def closest_enemy_to_flag(self):
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         Globals.blue_flag.x, Globals.blue_flag.y)
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         Globals.blue_flag.x, Globals.blue_flag.y)
            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance


