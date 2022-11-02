from ast import Global
from GameFrame import RedBot, Globals
import random
from enum import Enum
class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    JAIL_BREAK = 3

class Red3(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.initial_wait = random.randint(30, 90)
        self.wait_count = 0
        self.curr_state = STATE.WAIT
        self.set_image("Images/master.png", 25, 25)

    def tick(self):
        self.turn_towards(0, Globals.SCREEN_HEIGHT/2, 30)
        self.drive_forward(Globals.FAST)
    #     if self.curr_state == STATE.WAIT:
    #         self.wait()
    #     elif self.curr_state == STATE.ATTACK:
    #         self.attack()
    #     elif self.curr_state == STATE.JAIL_BREAK:
    #         self.jailbreak()
    #     else:
    #         self.curr_state = STATE.WAIT

    # def wait(self):
    #     bot, distance = self.closest_enemy_to_flag()
    #     if distance < 250:
    #         self.curr_state = STATE.ATTACK
    #     else:
    #         bot_jailed = False
    #         for team_bot in Globals.blue_bots:
    #             if team_bot.jailed:
    #                 bot_jailed = True
    #                 break
    #         if bot_jailed:
    #             self.curr_state = STATE.JAIL_BREAK

    # def attack(self):
    #     bot, distance = self.closest_enemy_to_flag()
    #     if distance < 250:
    #         self.turn_towards(bot.x, bot.y, Globals.FAST)
    #         self.drive_forward(Globals.FAST)
    #     else:
    #         self.curr_state = STATE.WAIT

    # def jailbreak(self):
    #     bot_jailed = False
    #     for team_bot in Globals.red_bots:
    #         if team_bot.jailed:
    #             bot_jailed = True
    #             break
    #     if not bot_jailed:
    #         self.curr_state = STATE.WAIT
    #     else:
    #         self.turn_towards(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT, Globals.FAST)
    #         self.drive_forward(Globals.FAST)

    # def closest_enemy_to_flag(self):
    #     closest_bot = Globals.red_bots[0]
    #     shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
    #                                                      Globals.red_flag.x, Globals.red_flag.y)
    #     for curr_bot in Globals.red_bots:
    #         curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
    #                                                      Globals.red_flag.x, Globals.red_flag.y)
    #         if curr_bot_dist < shortest_distance:
    #             shortest_distance = curr_bot_dist
    #             closest_bot = curr_bot

    #     return closest_bot, shortest_distance

