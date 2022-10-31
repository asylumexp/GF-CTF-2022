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

        self.curr_state = STATE.PINQLIANG

    def tick(self):

        if self.curr_state == STATE.PINQLIANG:
            self.PINQLIANG()
        if self.curr_state == STATE.HANDAN:
            self.HANDAN()
        if self.curr_state == STATE.TIANSHUI:
            self.TIANSHUI()
        print(self.x, self.y)


    def PINQLIANG(self):
        bot, distance = self.closest_enemy_to_flag()

        if distance < 150:
            self.curr_state = STATE.HANDAN
        else:
            self.turn_towards(Globals.SCREEN_WIDTH / 2, Globals.SCREEN_HEIGHT, Globals.SLOW)
            self.drive_forward(Globals.FAST)

        bot, distance = Globals.red_flag.x(), Globals.red_flag.y()

        if distance > 400:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.SLOW)
            self.drive_forward(Globals. FAST)






    def HANDAN(self):
        bot, distance = self.closest_enemy_to_flag()
        Globals.red_bots[4].x = self.x
        Globals.red_bots[4].y = self.y
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

    def wether_in_enemy(self):
        pass


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

        bot, distance = self.closest_enemy_to_bot()
        if distance > 250:
            self.curr_state = STATE.PINQLIANG

    def BAO (self):
        bot, distance = self.closest_enemy_to_bot()
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         Globals.red_bots[4].x, Globals.red_bots[4].y)

        if self.curr_state == STATE.PINQLAING and distance > 150:
            self.turn_towards(closest_bot.x *-1 / shortest_distance, closest_bot.y *-1 / shortest_distance, Globals.SLOW)
            self.drive_forward(Globals.FAST)

        else:
            self.curr_state = STATE.PINQLIANG

