from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    TIANSHUI = 0 # * Wait state
    HANDAN = 1 # * Strike state
    PINQLIANG = 2 # * Move to area state
    BAO = 3 # * Bait state
    BAIT_TRUE = 4 # * Prepare bait state
    EVADE = 5 # * Evade state
    JAIL = 6 # * Jail state

class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.set_image("Images/batman2.png", 25, 25)
        self.curr_state = STATE.TIANSHUI

    def tick(self):
        # * States
        if self.curr_state == STATE.PINQLIANG:
            self.PINQLIANG()
        elif self.curr_state == STATE.HANDAN:
            self.HANDAN()
        elif self.curr_state == STATE.TIANSHUI:
            self.TIANSHUI()
        elif self.curr_state == STATE.BAIT_TRUE:
            self.BAIT_TRUE()
        elif self.curr_state == STATE.EVADE:
            self.EVADE()
        elif self.curr_state == STATE.BAO:
            self.BAO()
        elif self.curr_state == STATE.JAIL:
            self.JAIL()
        else:
            self.curr_state = STATE.TIANSHUI


    # * Moving to prepare area
    def PINQLIANG(self):
        # * Drive until in position in upper region
        if self.x <= 644 or self.x >= 656:
            self.turn_towards(650, 25, Globals.FAST)
            self.drive_forward(Globals.FAST)
        # * If that the area, start the bait prepare
        else:
            self.curr_state = STATE.BAIT_TRUE

    # * Attack State
    def HANDAN(self):
        # * Check for bot
        bot, distance = self.closest_enemy_to_bot()
        angle = self.angleRelative(bot.x,bot.y)
        self.turn_towards(bot.x, bot.y, Globals.SLOW)
        if distance<100 and angle<70:
                self.drive_forward(Globals.FAST)
        if distance>100:
            self.curr_state = STATE.TIANSHUI

    # * Waiting for other bait bots
    def BAIT_TRUE(self):
        Globals.red_bots[0].bot5ready = True
        # if Globals.red_bots[0].bot3ready and Globals.red_bots[0].bot4ready:
        self.curr_state = STATE.BAO

    #  * Checking for enemies
    def TIANSHUI(self):
        bot, distance = self.closest_enemy_to_bot()
        if distance < 250:
            self.curr_state = STATE.HANDAN

        else:
            self.curr_state = STATE.PINQLIANG
            
    # * Bait state
    def BAO(self):
        if self.x >= 1200 and self.y >= 650:
            self.curr_state = STATE.JAIL
        bot, distance = self.closest_enemy_to_bot()
        distance = self.point_to_point_distance(self.x, self.y, bot.x, bot.y)
        if distance < 50:
            self.turn_left(Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif not self.has_flag:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.has_flag:
            self.turn_towards(Globals.red_bots[0].x, Globals.red_bots[0].y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            print("PASS, RED5 BAO()")
        # else:
        #     self.curr_state = STATE.EVADE

    # * Jail state
    def JAIL(self):
        # Globals.red_bots[0].bot5ready = False
        if not self.jailed:
            self.curr_state = STATE.TIANSHUI

    # * Evade state
    def EVADE(self):
        # ! WAITING ON CHARLIE OR SAMS EVADE CODE TO FINISH
        pass
    
    # ** Helper Functions **
    
    # * get closest enemy to self
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

    # * Get closest enemy to the flag
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
    
    # * Relative angle calculation
    def angleRelative(self,x,y):
        angle=self.NormalizedAngle(x,y)
        diffangle=min(abs(self.angle-angle),360-abs(self.angle-angle))
        return diffangle

    # * normalised angle calculation
    def NormalizedAngle(self,x,y):
        angle = self.get_rotation_to_coordinate(x,y)
        if angle<0: angle+=360
        return angle

#
# from GameFrame import RedBot, Globals
# from enum import Enum
#
#
# class STATE(Enum):
#     BAIT_TRUE = 4
#     TIANSHUI = 0 #wait
#     PINQLIANG = 2 #bait
#     HANDAN = 1 #strike
#     BAO = 3 #bait dodge
#     EVADE = 5 #exactly what the state says
#     JAIL = 6 #exactly what it says
#
#
# class Red5(RedBot):
#     def __init__(self, room, x, y):
#         RedBot.__init__(self, room, x, y)
#         self.set_image("Images/batman2.png", 25, 25)
#         self.curr_state = STATE.TIANSHUI
#         #boatman!!
#     def tick(self):
#         if self.curr_state == STATE.PINQLIANG:
#             self.PINQLIANG()
#         elif self.curr_state == STATE.HANDAN:
#             self.HANDAN()
#         elif self.curr_state == STATE.TIANSHUI:
#             self.TIANSHUI()
#         elif self.curr_state == STATE.BAIT_TRUE:
#             self.BAIT_TRUE()
#         elif self.curr_state == STATE.EVADE:
#             self.EVADE()
#         elif self.curr_state == STATE.BAO:
#             self.BAO()
#         elif self.curr_state == STATE.JAIL:
#             self.JAIL()
#         else:
#             self.curr_state = STATE.PINQLIANG
#
#
#
#     def PINQLIANG(self):
#         if self.x <= 644 or self.x >= 656:
#             self.turn_towards(650, 25, Globals.FAST)
#             self.drive_forward(Globals.FAST)
#         else:
#             self.curr_state = STATE.BAIT_TRUE
#
#
#
#
#     def HANDAN(self):
#         bot, distance = self.closest_enemy_to_bot()
#         angle = self.angleRelative(bot.x,bot.y)
#         self.turn_towards(bot.x, bot.y, Globals.SLOW)
#         if distance<100 and angle<70:
#                 self.drive_forward(Globals.FAST)
#         if distance>100:
#             self.curr_state = STATE.TIANSHUI
#
#     def BAIT_TRUE(self):
#         Globals.red_bots[0].bot5ready = True
#         if Globals.red_bots[0].bot3ready and Globals.red_bots[0].bot4ready:
#             self.curr_state = STATE.BAO
#
#     def closest_enemy_to_flag(self):
#         closest_bot = Globals.blue_bots[0]
#         shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
#                                                          Globals.blue_flag.x, Globals.blue_flag.y)
#         for curr_bot in Globals.blue_bots:
#             curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
#                                                          Globals.blue_flag.x, Globals.blue_flag.y)
#             if curr_bot_dist < shortest_distance:
#                 shortest_distance = curr_bot_dist
#                 closest_bot = curr_bot
#
#         return closest_bot, shortest_distance
#
#
#
#
#     def bot_ready_check(self):
#         return Globals.red_bots[0].bot_ready
#     #it works now
#
#
#
#     def closest_enemy_to_bot(self):
#         closest_bot = Globals.blue_bots[0]
#
#         shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
#                                                          Globals.red_bots[4].x, Globals.red_bots[4].y)
#         for curr_bot in Globals.blue_bots:
#
#             curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
#                                                          Globals.red_bots[4].x, Globals.red_bots[4].y)
#             if curr_bot_dist < shortest_distance:
#                 shortest_distance = curr_bot_dist
#                 closest_bot = curr_bot
#
#         return closest_bot, shortest_distance
#
#
#     def TIANSHUI(self):
#         bot, distance = self.closest_enemy_to_bot()
#         if distance < 250:
#             self.curr_state = STATE.HANDAN
#
#         else:
#             self.curr_state = STATE.PINQLIANG
#
#     def BAO (self):
#         if self.x >= 1200 and self.y >= 650:
#             self.curr_state = STATE.JAIL
#         bot, distance = self.closest_enemy_to_bot()
#         distance = self.point_to_point_distance(self.x, self.y, bot.x, bot.y)
#         # if distance < 50:
#         if not self.has_flag:
#             print("no flag", "red5")
#             self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
#             self.drive_forward(Globals.FAST)
#         elif self.has_flag:
#             print("flag", "red5")
#             self.turn_towards(Globals.red_bots[0].x, Globals.red_bots[0].y, Globals.FAST)
#             self.drive_forward(Globals.FAST)
#         else:
#             print("PASS, RED5 BAO()")
#         # else:
#         #     self.curr_state = STATE.EVADE
#
#     def JAIL(self):
#         Globals.red_bots[0].bot5ready = False
#         if not self.jailed:
#             self.curr_state = STATE.TIANSHUI
#
#
#
#
#     def EVADE(self):
#              # WAITING ON CHARLIE OR SAMS EVADE CODE TO FINISH
#         pass
#
#     def checkReady(self):
#         return Globals.red_bots[0].bot3ready, Globals.red_bots[0].bot4ready, Globals.red_bots[0].bot5ready
#
#     def angleRelative(self,x,y):
#         angle=self.NormalizedAngle(x,y)
#         diffangle=min(abs(self.angle-angle),360-abs(self.angle-angle))
#         return diffangle
#
#     def NormalizedAngle(self,x,y):
#         angle = self.get_rotation_to_coordinate(x,y)
#         if angle<0: angle+=360
#         return angle
#
#
#
#
#
#
# # from GameFrame import RedBot, Globals
# # from enum import Enum
# #
# #
# # class STATE(Enum):
# #     BAIT_TRUE = 4
# #     TIANSHUI = 0 #wait
# #     PINQLIANG = 2 #bait
# #     HANDAN = 1 #strike
# #     BAO = 3 #bait dodge
# #     EVADE = 5 #exactly what the state says
# #     JAIL = 6 #exactly what it says
# #
# #
# # class Red5(RedBot):
# #     def __init__(self, room, x, y):
# #         RedBot.__init__(self, room, x, y)
# #         self.set_image("Images/batman2.png", 25, 25)
# #         self.curr_state = STATE.TIANSHUI
# #         #boatman!!
# #     def tick(self):
# #         if self.curr_state == STATE.PINQLIANG:
# #             self.PINQLIANG()
# #         elif self.curr_state == STATE.HANDAN:
# #             self.HANDAN()
# #         elif self.curr_state == STATE.TIANSHUI:
# #             self.TIANSHUI()
# #         elif self.curr_state == STATE.BAIT_TRUE:
# #             self.BAIT_TRUE()
# #         elif self.curr_state == STATE.EVADE:
# #             self.EVADE()
# #         elif self.curr_state == STATE.BAO:
# #             self.BAO()
# #         elif self.curr_state == STATE.JAIL:
# #             self.JAIL()
# #         else:
# #             self.curr_state = STATE.PINQLIANG
# #
# #
# #
# #     def PINQLIANG(self):
# #         if self.x <= 644 or self.x >= 656:
# #             self.turn_towards(650, 25, Globals.FAST)
# #             self.drive_forward(Globals.FAST)
# #         else:
# #             self.curr_state = STATE.BAIT_TRUE
# #
# #
# #
# #
# #     def HANDAN(self):
# #         bot, distance = self.closest_enemy_to_bot()
# #         angle = self.angleRelative(bot.x,bot.y)
# #         self.turn_towards(bot.x, bot.y, Globals.SLOW)
# #         if distance<100 and angle<70:
# #                 self.drive_forward(Globals.FAST)
# #         if distance>100:
# #             self.curr_state = STATE.TIANSHUI
# #
# #     def BAIT_TRUE(self):
# #         Globals.red_bots[0].bot5ready = True
# #         if Globals.red_bots[0].bot3ready and Globals.red_bots[0].bot4ready:
# #             self.curr_state = STATE.BAO
# #
# #     def closest_enemy_to_flag(self):
# #         closest_bot = Globals.blue_bots[0]
# #         shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
# #                                                          Globals.blue_flag.x, Globals.blue_flag.y)
# #         for curr_bot in Globals.blue_bots:
# #             curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
# #                                                          Globals.blue_flag.x, Globals.blue_flag.y)
# #             if curr_bot_dist < shortest_distance:
# #                 shortest_distance = curr_bot_dist
# #                 closest_bot = curr_bot
# #
# #         return closest_bot, shortest_distance
# #
# #
# #
# #
# #     def bot_ready_check(self):
# #         return Globals.red_bots[0].bot_ready
# #     #it works now
# #
# #
# #
# #     def closest_enemy_to_bot(self):
# #         closest_bot = Globals.blue_bots[0]
# #
# #         shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
# #                                                          Globals.red_bots[4].x, Globals.red_bots[4].y)
# #         for curr_bot in Globals.blue_bots:
# #
# #             curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
# #                                                          Globals.red_bots[4].x, Globals.red_bots[4].y)
# #             if curr_bot_dist < shortest_distance:
# #                 shortest_distance = curr_bot_dist
# #                 closest_bot = curr_bot
# #
# #         return closest_bot, shortest_distance
# #
# #
# #     def TIANSHUI(self):
# #         bot, distance = self.closest_enemy_to_bot()
# #         if distance < 250:
# #             self.curr_state = STATE.HANDAN
# #
# #         else:
# #             self.curr_state = STATE.PINQLIANG
# #
# #     def BAO (self):
# #         if self.x >= 1200 and self.y >= 650:
# #             self.curr_state = STATE.JAIL
# #         bot, distance = self.closest_enemy_to_bot()
# #         distance = self.point_to_point_distance(self.x, self.y, bot.x, bot.y)
# #         # if distance < 50:
# #         if not self.has_flag:
# #             print("no flag", "red5")
# #             self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
# #             self.drive_forward(Globals.FAST)
# #         elif self.has_flag:
# #             print("flag", "red5")
# #             self.turn_towards(Globals.red_bots[0].x, Globals.red_bots[0].y, Globals.FAST)
# #             self.drive_forward(Globals.FAST)
# #         else:
# #             print("PASS, RED5 BAO()")
# #         # else:
# #         #     self.curr_state = STATE.EVADE
# #
# #     def JAIL(self):
# #         Globals.red_bots[0].bot5ready = False
# #         if not self.jailed:
# #             self.curr_state = STATE.TIANSHUI
# #
# #
# #
# #
# #     def EVADE(self):
# #              # WAITING ON CHARLIE OR SAMS EVADE CODE TO FINISH
# #         pass
# #
# #     def checkReady(self):
# #         return Globals.red_bots[0].bot3ready, Globals.red_bots[0].bot4ready, Globals.red_bots[0].bot5ready
# #
# #     def angleRelative(self,x,y):
# #         angle=self.NormalizedAngle(x,y)
# #         diffangle=min(abs(self.angle-angle),360-abs(self.angle-angle))
# #         return diffangle
# #
# #     def NormalizedAngle(self,x,y):
# #         angle = self.get_rotation_to_coordinate(x,y)
# #         if angle<0: angle+=360
# #         return angle
# #

