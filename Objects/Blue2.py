from GameFrame import BlueBot, Globals
from enum import Enum 


class STATE(Enum):
    DEFEND = 0
    RETURN = 1
    ATTACK = 2
    SAVE = 3

class Blue2(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)

        self.curr_state = STATE.RETURN

        
    def tick(self):
        if self.curr_state == STATE.DEFEND:
            self.defend()
        elif self.curr_state == STATE.RETURN:
            self.home()
        elif self.curr_state == STATE.ATTACK:
            self.attack()
        elif self.curr_state == STATE.SAVE:
            self.save()
        else: 
            self.curr_state = STATE.RETURN
        print(self.curr_state)
        
            
#STATE Functions 

    def defend(self):
        closest_bot = self.closest_enemy()
        point_distance = self.point()
        #lineturn = Blue1.curr_rotation

        # if an enemy is less than x and y from flag 
        #change tto Attack state 
        if self.enemy_in_danger_zone():
            print("Enemy in Danger Zone")
            self.curr_state = STATE.ATTACK

        # if a team bot is jailed and enemy is more than x and y from flag
        #change to save state
        elif self.tean_mate_in_jail() == True and closest_bot.x >= Globals.SCREEN_WIDTH/2:
            self.curr_state = STATE.SAVE


        #Move to a New Point on the path which is closest to the enemy which is within the closest X and Y from the flag
        #turn towards enemy
        
        #elif lineturn >< 0:
            #self.turn_left(10, Globals.SLOW)

            
        else: 
            self.turn_towards(closest_bot.x, closest_bot.y, Globals.FAST)
        
    def home(self):
        closest_bot = self.closest_enemy()
        point_distance = self.point()

        if self.enemy_in_danger_zone():
            print("Enemy in Danger Zone")
            self.curr_state = STATE.ATTACK
        
        elif self.tean_mate_in_jail() == True and closest_bot.x >= Globals.SCREEN_WIDTH/2:
            self.curr_state = STATE.SAVE
        
        elif point_distance > 15 and self.x < Globals.SCREEN_WIDTH/2:
            self.turn_towards(Globals.red_flag.x - 5, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.MEDIUM)
            
        elif point_distance < 15 and self.x < Globals.SCREEN_WIDTH/2:
            self.curr_state = STATE.DEFEND


    
    def attack(self):
        closest_bot = self.closest_enemy()
        #Enemy more than X and Y from the flag
        #change to defend state
        if not self.enemy_in_danger_zone(): 
            self.curr_state = STATE.RETURN


        #Turn towards the enemy
        #attack
        elif self.x >= Globals.SCREEN_WIDTH/2:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.SLOW)

        elif closest_bot.x <= Globals.SCREEN_WIDTH/2:       
            self.turn_towards(closest_bot.x, closest_bot.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        
        

            #self.turn_towards(closest_bot.x, closest_bot.y, Globals.Fast)
            #self.drive_forward(Globals.SLOW)

            


    def save(self):
        #team bot is saved
        #change to defend state
        if not self.tean_mate_in_jail():
            self.curr_state = STATE.RETURN

    
        #Enemy less than X and Y from the flag
        #change to attack state
        elif self.enemy_in_danger_zone():
            self.curr_state = STATE.ATTACK

        #move towards jailed bot and release him
        else:
            for bot in Globals.blue_bots:
                if bot.jailed:
                    self.turn_towards(bot.x, bot.y, Globals.FAST)
                    self.drive_forward(Globals.FAST)
                    break



        

# Helper Function

    def enemy_in_danger_zone(self):
        in_danger = False
        for bot in Globals.red_bots:
            distance = self.point_to_point_distance(
                bot.x, bot.y, 
                Globals.red_flag.x, Globals.red_flag.y
                )
            if distance < 40:
                in_danger = True
                break
        return in_danger

    def enemy_in_warning_zone(self):
        in_warning = False
        for bot in Globals.red_bots:
            distance = self.point_to_point_distance(
                bot.x, bot.y, 
                Globals.red_flag.x, Globals.red_flag.y
                )
            if distance < 400:
                in_warning = True
                break
        return in_warning

    def tean_mate_in_jail(self):
        jailed = False
        for bot in Globals.blue_bots:
            if bot.jailed:
                jailed = True
                break
        return jailed 

    def closest_enemy(self):
        closest_bot = Globals.red_bots[0]
        distance = self.point_to_point_distance(
            closest_bot.x, closest_bot.y, 
            Globals.red_flag.x, Globals.red_flag.y
            )
        
        for bot in Globals.red_bots:
            bot_distance = self.point_to_point_distance(
            bot.x, bot.y, 
            Globals.red_flag.x, Globals.red_flag.y
            )
            if bot_distance < distance:
                distance = bot_distance
                closest_bot = bot
        return closest_bot

    def point(self):
        point_distance = self.point_to_point_distance(Globals.red_flag.x - 5, Globals.red_flag.y, self.x, self.y)
        return point_distance
        
    def closest(self):
        bot_distances = []
        for bots in Globals.red_bots:
            distance = bots.point_to_point_distance(Globals.red_flag.x,Globals.red_flag.y,bots.x,bots.y)
            bot_distances.append(distance)
            bot_distances.sort()


    
    
    
        
