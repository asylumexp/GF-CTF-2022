from GameFrame import BlueBot, Globals
from enum import Enum
import math 
import random

class STATE(Enum):
    ATTACK = 1
    EVADE = 2
    RETURN = 3


class Blue5(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)

        self.halfway = Globals.SCREEN_WIDTH / 2

        self.curr_state = STATE.ATTACK


    def tick(self):
        if self.curr_state == STATE.ATTACK:
            self.attack()
        elif self.curr_state == STATE.EVADE:
            self.evade()
        elif self.curr_state == STATE.RETURN:
            self.returnFlag()
        else:
            self.curr_state = STATE.ATTACK

        
       
        
    
    def attack(self):
        distance = self.distanceToFlag()
        closest_bot, dist = self.closest_enemy()
        dist_to_point = self.point_to_point_distance(self.x, self.y,
                Globals.blue_flag.x + 500, Globals.blue_flag.y + 200)
        if distance > 100:
            if dist_to_point > 400:
                if dist > 100:
                    self.turn_towards(Globals.blue_flag.x + 500, Globals.blue_flag.y + 200)
                    self.drive_forward(Globals.FAST)
                if dist < 100:
                    if self.x < 600:
                        self.turn_towards(closest_bot.x, closest_bot.y,Globals.FAST)
                        self.drive_forward(Globals.FAST)
                    else:
                        self.curr_state = STATE.EVADE
            elif dist_to_point < 400:
                if dist > 100:
                    self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
                    self.drive_forward(Globals.FAST)
                if dist < 100:
                    if self.x < 600:
                        self.turn_towards(closest_bot.x,closest_bot.y,Globals.FAST)
                        self.drive_forward(Globals.FAST)
                    else:
                        self.curr_state = STATE.EVADE
        elif distance < 100:
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
            if self.has_flag == True:
                self.curr_state = STATE.RETURN

    def evade(self):
        distance_to_flag = self.point_to_point_distance(self.x, self.y,
                             Globals.blue_flag.x, Globals.blue_flag.y)
        pointX, pointY = self.oppositeDirection()
        closest_bot, dist = self.closest_enemy()
        if dist > 100:
            self.curr_state = STATE.ATTACK
        elif dist < 100:
            if self.y < 100:
                self.turn_towards(self.x - 100, self.y + 100)
                self.drive_forward(Globals.FAST)
            elif self.y > 650:
                self.turn_towards(self.x - 100, self.y - 100)
                self.drive_forward(Globals.FAST)
            else:
                self.turn_towards(self.x + pointX, self.y + pointY, Globals.FAST)
                self.drive_forward(Globals.FAST)
        elif distance_to_flag < 100:
            self.curr_state = STATE.ATTACK


    def returnFlag(self):
        pointX,pointY = self.oppositeDirection()
        closest_bot, dist = self.closest_enemy()
        if dist > 100:
            self.turn_towards(self.x - 1000,360 + pointY,Globals.FAST)
            self.drive_forward(Globals.FAST)
            if self.has_flag == False:
                self.curr_state = STATE.ATTACK
        elif dist < 100:
            self.turn_towards(self.x + pointX, self.y + pointY, Globals.FAST)
            self.drive_forward(Globals.FAST)
            if self.has_flag == False:
                self.curr_state = STATE.ATTACK
            elif self.y > 650:
                self.turn_towards(320, 360,Globals.FAST)
                self.drive_forward(Globals.FAST)
            elif self.y < 100:
                self.turn_towards(320, 360,Globals.FAST)
                self.drive_forward(Globals.FAST)
        

    def closest_enemy(self):
        closest_bot = Globals.red_bots[1]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y, Globals.blue_bots[4].x,Globals.blue_bots[4].y)
        for testing_bot in Globals.red_bots:
            testing_bot_dist = self.point_to_point_distance(testing_bot.x,testing_bot.y,Globals.blue_bots[4].x,Globals.blue_bots[4].y)
            if testing_bot_dist < shortest_distance:
                shortest_distance = testing_bot_dist
                closest_bot = testing_bot
            return closest_bot,shortest_distance
        
    def distanceToFlag(self):
        distance = self.point_to_point_distance(self.x, self.y, Globals.blue_flag.x, Globals.blue_flag.y)
        return distance


    def oppositeDirection(self):
        closest_bot, dist = self.closest_enemy()
        pointX = self.x - closest_bot.x
        pointY = self.y - closest_bot.y
        return pointX,pointY
        

    



    
