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
        self.red4ready = False

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
        flagAngle=self.angleRelative(Globals.blue_flag.x,Globals.blue_flag.y)
        if distance<450:
            self.curr_state=STATE.STRIKE
        elif self.point_to_point_distance(self.x, self.y, Globals.blue_flag.x, Globals.blue_flag.y)>20:

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
        angle = self.angleRelative(bot.x,bot.y)
        self.turn_towards(bot.x, bot.y, Globals.FAST)
        if distance<100 and angle<70:
                self.drive_forward(Globals.FAST)
        if distance>100:
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
    def angleRelative(self,x,y):
        angle=self.NormalizedAngle(x,y)
        diffangle=min(abs(self.angle-angle),360-abs(self.angle-angle))
        return diffangle
    def NormalizedAngle(self,x,y):
        angle = self.get_rotation_to_coordinate(x,y)
        if angle<0: angle+=360
        return angle


