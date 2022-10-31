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


        self.curr_state = STATE.TIANSHUI

    def tick(self):
        print(self.curr_state)

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
            self.curr_state = STATE.HANDAN

        #inital bait movement waiting for other bots to be ready

        ready3, ready4 = self.checkReady()
        if ready3 and ready4:
            self.bot5ready = True
            self.curr_state = STATE.BAO

        else:
            self.turn_towards(Globals.SCREEN_WIDTH / 2, Globals.SCREEN_HEIGHT, Globals.SLOW)
            self.drive_forward(Globals.SLOW)
            self.curr_state = STATE.TIANSHUI


    def HANDAN(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250 and self.x == 255 and self.y == 255:
            self.turn_towards(bot.x, bot.y, Globals.SLOW)
            self.drive_forward(Globals.FAST)
        else:
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
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.curr_state = STATE.HANDAN

        else:
            self.curr_state = STATE.PINQLIANG

    def BAO (self):
       pass

        # WAITING ON CHARLIE OR SAMES EVADE CODE TO FINISH



    def checkReady(self):
        return Globals.red_bots[0].red3ready, Globals.red_bots[0].red4ready

