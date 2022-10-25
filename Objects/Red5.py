from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    TIANSHUI = 0 #wait
    PINQLIANG = 2 #bait
    HANDAN = 1 #strike



class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)

        self.curr_state = STATE.TIANSHUI

    def tick(self):

        if self.curr_state == STATE.PINQLIANG:
            self.PINQLIANG()
        if self.curr_state == STATE.HANDAN:
            self.HANDAN()
        if self.curr_state == STATE.TIANSHUI:
            self.TIANSHUI()


    def PINQLIANG(self):
        bot, distance = self.closest_enemy_to_bot()
        if distance < 250:
            self.curr_state = STATE.HANDAN
        else:
                pass




    def HANDAN(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
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
        elif distance > 250:
            self.set_timer(100, self.PINQLIANG)
            self.curr_state = STATE.PINQLIANG
