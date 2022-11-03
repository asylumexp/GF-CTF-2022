from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    FLAG = 3
    PREPARE = 4
    BAIT = 5
    JAIL = 6
    HOME = 7


class Red3(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.set_image("Images/master.png", 25, 25)
        self.curr_state = STATE.WAIT
        self.prev_x_enemy = 0

    def tick(self):
        if self.curr_state == STATE.WAIT:
            self.wait()
        elif self.curr_state == STATE.ATTACK:
            self.attack()
        elif self.curr_state == STATE.FLAG:
            self.flag()
        elif self.curr_state == STATE.PREPARE:
            self.prepare()
        elif self.curr_state == STATE.BAIT:
            self.bait()
        elif self.curr_state == STATE.JAIL:
            self.jailedf()
        elif self.curr_state == STATE.HOME:
            self.gohome()
        else:
            self.curr_state = STATE.WAIT
    # 
    def wait(self):
        bot, distance = self.closest_enemy_to_flag()
        #Stay and or move close to the top border
        if self.x <= 644 or self.x >= 656:
            self.turn_towards(650, 50, Globals.FAST)
            self.drive_forward(Globals.FAST)
        # todo Check for enemies
        # if distance < 250 and bot.x > 650:
        #     self.curr_state = STATE.ATTACK
        # todo Wait for Bait
        
        else:
            print("else")
            self.curr_state = STATE.PREPARE
            # * self.curr_state = STATE.FLAG
    
    def prepare(self):
        Globals.red_bots[0].bot3ready = True
        if Globals.red_bots[0].bot4ready and Globals.red_bots[0].bot5ready:
            self.curr_state = STATE.BAIT

    def bait(self):
        if self.x >= 1200 and self.y >= 650:
            self.curr_state = STATE.JAIL
        bot, distance = self.closest_enemy_to_flag()
        # ? move across border, evading enemies
        self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
        # todo keep enemies away from bot three
        if distance < 250:
            self.evadeBots()
        # * if no enemies are attacking self
        else:
            self.attackFLAG()
    
    def attackFLAG(self):
        # * If tagged:
        if self.jailed:
            self.curr_state = STATE.JAIL
        # todo - evade enemies
        self.evadeBots()
        # todo - move to flag
        # todo - return with flag
        self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
        self.drive_forward(Globals.FAST)

    
    def jailedf(self):
        # todo - if jailbroken
        Globals.red_bots[0].bot3ready = False
        if not self.jailed:
            self.curr_state = STATE.HOME
    
    def gohome(self):
        # todo - move to upper position
        self.curr_state = STATE.WAIT
    
    def attack(self):
        # todo - attack bots
        
        # todo - return to previous function
        pass
    
    """
    Helper Functions
    """
    
    def evadeBots(self):
        pass
        # # todo - evade bot
        # bot, dist = self.closest_enemy_to_self(True)
        # startMOVING = False
        # if self.curr_rotation <= bot.curr_rotation + 9 and self.curr_rotation >= bot.curr_rotation - 9:
        #     startMOVING = True
        # elif self.curr_rotation <= 180:
        #     if self.curr_rotation + 2 < bot.curr_rotation < self.curr_rotation + 180:
        #         self.turn_left(Globals.FAST)
        #     else:
        #         self.turn_right(Globals.FAST)
        # else:
        #     if self.curr_rotation + 2 < bot.curr_rotation < 360 or 0 <= bot.curr_rotation < self.curr_rotation - 180:
        #         self.turn_left(Globals.FAST)
        #     else:
        #         self.turn_right(Globals.FAST)
        # if startMOVING == True:
        #     self.drive_forward(Globals.FAST)
            
             
        
        
        

    def attack(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.turn_towards(bot.x, bot.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.curr_state = STATE.WAIT

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
    
    def closest_enemy_to_self(self, ignore):
        # todo - make more efficient
        closest_bot = Globals.blue_bots[0]
        closer_bot = Globals.red_bots[0] 
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         self.x, self.y)
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         self.x, self.y)
            for red_bot in Globals.red_bots:
                # * check enemy distance from self to bot from loop
                if curr_bot_dist < shortest_distance:
                    curr_teammate_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         self.x, self.y)
                    # * check if teammate is closer
                    if curr_teammate_dist < curr_bot_dist and not ignore:
                        shortest_distance = curr_bot_dist
                        closest_bot = curr_bot
                    elif ignore:
                        shortest_distance = curr_bot_dist
                        closest_bot = curr_bot

        return closest_bot, shortest_distance
    
    def flag(self):
        if self.has_flag:
            self.turn_towards(Globals.SCREEN_WIDTH, self.y)
            self.drive_forward(Globals.FAST)
        elif self.rect.right >= Globals.SCREEN_WIDTH / 2:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)



# from ast import Global
# from GameFrame import RedBot, Globals
# import random
# from enum import Enum
# class STATE(Enum):
#     WAIT = 1
#     ATTACK = 2
#     JAIL_BREAK = 3

# class Red3(RedBot):
#     def __init__(self, room, x, y):
#         RedBot.__init__(self, room, x, y)
#         self.initial_wait = random.randint(30, 90)
#         self.wait_count = 0
#         self.curr_state = STATE.WAIT
#         self.set_image("Images/master.png", 25, 25)

#     def tick(self):
#         self.turn_towards(0, Globals.SCREEN_HEIGHT/2, 30)
#         self.drive_forward(Globals.FAST)
#     #     if self.curr_state == STATE.WAIT:
#     #         self.wait()
#     #     elif self.curr_state == STATE.ATTACK:
#     #         self.attack()
#     #     elif self.curr_state == STATE.JAIL_BREAK:
#     #         self.jailbreak()
#     #     else:
#     #         self.curr_state = STATE.WAIT

#     # def wait(self):
#     #     bot, distance = self.closest_enemy_to_flag()
#     #     if distance < 250:
#     #         self.curr_state = STATE.ATTACK
#     #     else:
#     #         bot_jailed = False
#     #         for team_bot in Globals.blue_bots:
#     #             if team_bot.jailed:
#     #                 bot_jailed = True
#     #                 break
#     #         if bot_jailed:
#     #             self.curr_state = STATE.JAIL_BREAK

#     # def attack(self):
#     #     bot, distance = self.closest_enemy_to_flag()
#     #     if distance < 250:
#     #         self.turn_towards(bot.x, bot.y, Globals.FAST)
#     #         self.drive_forward(Globals.FAST)
#     #     else:
#     #         self.curr_state = STATE.WAIT

#     # def jailbreak(self):
#     #     bot_jailed = False
#     #     for team_bot in Globals.red_bots:
#     #         if team_bot.jailed:
#     #             bot_jailed = True
#     #             break
#     #     if not bot_jailed:
#     #         self.curr_state = STATE.WAIT
#     #     else:
#     #         self.turn_towards(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT, Globals.FAST)
#     #         self.drive_forward(Globals.FAST)

#     # def closest_enemy_to_flag(self):
#     #     closest_bot = Globals.red_bots[0]
#     #     shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
#     #                                                      Globals.red_flag.x, Globals.red_flag.y)
#     #     for curr_bot in Globals.red_bots:
#     #         curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
#     #                                                      Globals.red_flag.x, Globals.red_flag.y)
#     #         if curr_bot_dist < shortest_distance:
#     #             shortest_distance = curr_bot_dist
#     #             closest_bot = curr_bot

#     #     return closest_bot, shortest_distance

