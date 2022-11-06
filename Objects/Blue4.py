from GameFrame import BlueBot, Globals
import math
import random
from enum import Enum


class STATE(Enum):
    ATTACK = 1
    DEFEND = 2
    EVADE = 3
    RETURN = 4



class Blue4(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.curr_state = STATE.ATTACK
        self.halfway = Globals.SCREEN_WIDTH / 2

    def tick(self):
        if self.curr_state == STATE.ATTACK:
            self.attack()
        elif self.curr_state == STATE.DEFEND:
            self.defend()
        elif self.curr_state == STATE.EVADE:
            self.evade()
        elif self.curr_state == STATE.RETURN:
            self.return_flag()
        else:
            self.curr_state = STATE.ATTACK
    

    def attack(self):
        enemy_has_flag, flag_enemy = self.enemy_has_flag()
        x,y = self.attackDirection()
        distance_to_flag = self.point_to_point_distance(self.x, self.y,
                             Globals.blue_flag.x, Globals.blue_flag.y)
        dist_to_point = self.point_to_point_distance(self.x,self.y,x,y)
        closest_enemy, dist = self.closest_enemy()
        enemies_in_area = self.amountOfEnemiesInArea()
        if dist_to_point > 400:
            self.turn_towards(x,y,Globals.FAST)
            self.drive_forward(Globals.FAST)
            if enemies_in_area < 3:
                self.curr_state = STATE.DEFEND
            elif dist < 100:
                if self.x > 600:
                    self.curr_state = STATE.EVADE
                else:
                    self.curr_state = STATE.DEFEND
            elif enemy_has_flag:
                self.curr_state = STATE.DEFEND
        if dist_to_point < 400:
            if distance_to_flag > 100:
                self.turn_towards(Globals.blue_flag.x,
                    Globals.blue_flag.y,Globals.FAST)
                self.drive_forward(Globals.FAST)
            elif distance_to_flag < 100:
                self.turn_towards(Globals.blue_flag.x,
                    Globals.blue_flag.y,Globals.FAST)
                self.drive_forward(Globals.FAST)
                if self.has_flag == True:
                    self.curr_state = STATE.RETURN
                elif dist < 100:
                    self.curr_state = STATE.EVADE

    def defend(self):
        enemy_has_flag, flag_enemy = self.enemy_has_flag()
        closest_enemy, dist = self.closest_enemy()
        enemies_in_area = self.amountOfEnemiesInArea()
        if enemy_has_flag == False:
            if enemies_in_area > 3:
                self.curr_state = STATE.ATTACK
            elif self.x > self.halfway - 100:
                self.turn_towards(self.halfway - 200,
                                 self.y, Globals.FAST)
                self.drive_forward(Globals.FAST)
            elif self.x < self.halfway:
                self.turn_towards(closest_enemy.x,
                    closest_enemy.y,Globals.FAST)
                self.drive_forward(Globals.FAST)
        elif enemy_has_flag:
            self.turn_towards(flag_enemy.x,
                flag_enemy.y,Globals.FAST)
            self.drive_forward(Globals.FAST)


    def evade(self):
        enemy_has_flag, flag_enemy = self.enemy_has_flag()
        distance_to_flag = self.point_to_point_distance(self.x, self.y, Globals.blue_flag.x, Globals.blue_flag.y)
        closest_enemy, dist = self.closest_enemy()
        enemies_in_area = self.amountOfEnemiesInArea()
        pointX, pointY = self.oppositeDirection()
        if dist < 100:
            if self.y > 650:
                self.turn_towards(self.x - 100,self.y + 100,Globals.FAST)
                self.drive_forward(Globals.FAST)
            elif self.y < 100:
                self.turn_towards(self.x - 100, self.y - 100,Globals.FAST)
                self.drive_forward(Globals.FAST)
            else:
                self.turn_towards(self.x + pointX, self.y + pointY, Globals.FAST)
                self.drive_forward(Globals.FAST)
        elif dist > 100:
            self.curr_state = STATE.ATTACK
        elif distance_to_flag < 100:
            self.curr_state = STATE.ATTACK
        elif enemy_has_flag:
            self.curr_state = STATE.DEFEND

    

    def return_flag(self):
        pointX,pointY = self.oppositeDirection()
        closest_bot, dist = self.closest_enemy()
        if dist > 100:
            self.turn_towards(self.x - 1000,360 + pointY, Globals.FAST)
            self.drive_forward(Globals.FAST)
            if self.has_flag == False:
                self.curr_state = STATE.ATTACK
        if dist < 100:
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

    def amountOfEnemiesInArea(self):
        closeBots = []
        for bot in Globals.red_bots:
            if bot.x > 0:
                closeBots.append(bot)
                if bot.x < 800:
                    closeBots.remove(bot)
        return len(closeBots)

    def oppositeDirection(self):
        closest_bot, dist = self.closest_enemy()
        pointX = self.x - closest_bot.x
        pointY = self.y - closest_bot.y
        return pointX,pointY

    def closest_enemy(self):
        closest_bot = Globals.red_bots[1]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,self.x,self.y)
        for testing_bot in Globals.red_bots:
            testing_bot_dist = self.point_to_point_distance(testing_bot.x,testing_bot.y,self.x,self.y)
            if testing_bot_dist < shortest_distance:
                shortest_distance = testing_bot_dist
                closest_bot = testing_bot
            return closest_bot,shortest_distance
    
    def closest_enemy_to_flag(self):
        closest_bot = Globals.red_bots[1]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y, Globals.blue_flag.x,Globals.blue_flag.y)
        for testing_bot in Globals.red_bots:
            testing_bot_dist = self.point_to_point_distance(testing_bot.x,testing_bot.y,Globals.blue_flag.x,Globals.blue_flag.y)
            if testing_bot_dist < shortest_distance:
                shortest_distance = testing_bot_dist
                closest_bot = testing_bot
            return closest_bot,shortest_distance
    
    def attackDirection(self):
        closest_enemy_at_flag ,dist = self.closest_enemy_to_flag()
        if closest_enemy_at_flag.y < Globals.blue_flag.y:
            X = Globals.blue_flag.x + 400
            Y = Globals.blue_flag.y + 200
        else:
            X = Globals.blue_flag.x + 400
            Y = Globals.blue_flag.y - 200
        return X, Y


    def enemy_has_flag(self):
        enemyHasFlag = False
        for bot in Globals.red_bots:
            if bot.has_flag:
                enemyHasFlag = True
        return enemyHasFlag,bot