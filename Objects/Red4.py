from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    FLAG = 3


class Red4(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.set_image("Images/master.png", 25, 25)
        self.curr_state = STATE.WAIT

    def tick(self):
        if self.curr_state == STATE.WAIT:
            self.wait()
        elif self.curr_state == STATE.ATTACK:
            self.attack()
        elif self.curr_state == STATE.FLAG:
            self.flag()
        else:
            self.curr_state = STATE.WAIT

    def wait(self):
        bot, distance = self.closest_enemy_to_flag()
        #Stay and or move close to the top border
        
        # Check for enemies
        if distance < 250:
            self.curr_state = STATE.ATTACK
        #Wait for Bait
        else:
            self.curr_state = STATE.FLAG
    
    def bait():
        #move across border, evading enemies
        
        # keep enemies away from bot three
        
        #if no enemies are attacking self
        pass
    
    def attackFLAG():
        #evade enemies
        
        #move to flag
        
        #return with flag
        
        #if tagged
        pass
    
    def jailed():
        #if jailbroken
        pass
    
    def gohome():
        #move to upper position
        
        #if enemies are nearby
        pass
    
    def attack():
        #attack bots
        
        #return to previous function
        pass
    
    """
    Helper Functions
    """
    
    def evadeBots():
        #evade bot
        pass
        
        

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