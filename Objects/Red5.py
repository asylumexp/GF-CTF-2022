from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    TIANSHUI = 0 #wait
    PINQLIANG = 2 #bait
    HANDAN = 1 #strike
    BAO = 3 #bait dodge



class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.set_image("Images/batman2.png", 25, 25)
        self.curr_state = STATE.TIANSHUI
        #boatman!!
    def tick(self):
        # print(self.curr_state)

        if self.curr_state == STATE.PINQLIANG:
            self.PINQLIANG()
        elif self.curr_state == STATE.HANDAN:
            self.HANDAN()
        elif self.curr_state == STATE.TIANSHUI:
            self.TIANSHUI()
        else:
            self.curr_state = STATE.PINQLIANG



    def PINQLIANG(self):
        distance = self.point_to_point_distance(self.x, self.y, Globals.blue_bots[0].x, Globals.blue_bots[0].y)
        if distance < 250:
            Globals.red_bots[0].bot5ready = False
            self.curr_state = STATE.HANDAN
        elif not self.x >= 635 or not self.x <= 650:
            print("bot 5 moving")
            self.turn_towards(650, 80, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.x >= 635 and self.x <= 650:
            Globals.red_bots[0].bot5ready = True
            print("bot 5 ready")

        #inital bait movement waiting for other bots to be ready

        ready3, ready4, ready5 = self.checkReady()
        print(ready3, ready4, ready5)
        if ready3 and ready4 and ready5:
            self.curr_state = STATE.BAO



    def HANDAN(self):
        bot, distance = self.closest_enemy_to_bot()
        angle = self.angleRelative(bot.x,bot.y)
        self.turn_towards(bot.x, bot.y, Globals.SLOW)
        if distance<100 and angle<70:
                self.drive_forward(Globals.FAST)
        if distance>100:
            self.curr_state = STATE.TIANSHUI


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




    def bot_ready_check(self):
        return Globals.red_bots[0].bot_ready
    #it works now



    def closest_enemy_to_bot(self):
        closest_bot = Globals.blue_bots[0]

        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         Globals.red_bots[4].x, Globals.red_bots[4].y)
        for curr_bot in Globals.blue_bots:

            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         Globals.red_bots[4].x, Globals.red_bots[4].y)
            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance


    def TIANSHUI(self):
        bot, distance = self.closest_enemy_to_bot()
        if distance < 250:
            self.curr_state = STATE.HANDAN

        else:
            self.curr_state = STATE.PINQLIANG

    def BAO (self):
        bot = Globals.red_flag()
        angle = self.angleRelative(bot.x, bot.y)
        self.turn_towards(bot.x, bot.y, Globals.SLOW)
        if angle <= 70:
                self.drive_forward(Globals.FAST)
        elif angle >= 70:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)


        # WAITING ON CHARLIE OR SAMS EVADE CODE TO FINISH



    def checkReady(self):
        return Globals.red_bots[0].bot3ready, Globals.red_bots[0].bot4ready, Globals.red_bots[0].bot5ready

    def angleRelative(self,x,y):
        angle=self.NormalizedAngle(x,y)
        diffangle=min(abs(self.angle-angle),360-abs(self.angle-angle))
        return diffangle

    def NormalizedAngle(self,x,y):
        angle = self.get_rotation_to_coordinate(x,y)
        if angle<0: angle+=360
        return angle

