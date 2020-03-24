import random
import math
import time

xp = [x*10 for x in range(100)] # xp use to level up
drop ={
       0: [1, 0.4], #potion
       1: [4, 0.3], #focuscard
       2: [6, 0.15], #Evadecard
       3: [7, 0.1], #BackStab
       }

class System:
    def __init__(self, player, monster, cardPile):
        self.player = player
        self.monster = monster
        self.turn = 0
        self.cardPile = cardPile
    def getTurn(self):
        return self.turn
    def endTurn(self):
        print("System: end turn {}\n".format(self.turn))
        self.monster.attack(self.player)
        self.player.initTurn()
        self.turn += 1
        time.sleep(1)
        print("\n---------System: turn {}---------\n".format(self.turn))
        
    def test(self):
        print("\n====testing====")
        print("\nSystem: turn {}".format(self.turn))
        self.player.equip("Armour", "Leather Armour", 2)
        self.player.equip("Weapon", "Wooden Sword", 3)
        while(not self.monster.isDead()):
            self.player.attack(self.monster)
            self.endTurn()
            if (self.player.isDead()):
                break
        print("\n====DONE====")
        
    def battle(self):
        print("===Battle Start===")
        print("\n--System: turn {}--\n".format(self.getTurn()))
        self.cardPile.shuffle()
        self.monster.showInfo()
        while(1):
            if self.monster.isDead(): break
            self.cardPile.init()
            print("\nSystem: drawed cards on hand\n")
            self.cardPile.showCard()
            print("\nSystem: use command *if you use you can't play any card in this turn")
            self.player.showHpMp()
            self.monster.showHp()
            print("0: Don't use command")
            print("1: Rest recover 5 mp")
            print("2: Discard all card on hand")
            useRest = int(input("Use: "))
            if useRest == 1:
                self.player.rest()
            elif useRest == 2:
                self.cardPile.resetOnhand()
            while(useRest==0):
                if self.monster.isDead(): break
                time.sleep(0.5)
                print("")
                self.player.showHpMp()
                self.monster.showHp()
                self.cardPile.showCard()
                use = input("type ID to use [-1 to end turn]: ")
                if int(use) == -1: break
                self.cardPile.use(use)
                time.sleep(1)
                if self.cardPile.getLenOnhand() == 0:
                    break
                time.sleep(0.5)
            print("System: 4 mp recovered ")
            self.endTurn()
            time.sleep(1)
        if self.monster.isDead():
            xp = self.monster.getXp()
            self.player.levelUp(xp)
            item = self.monster.getDrop()
            if item != -1:
                print("System: receive item [{}]".format(item))
                self.cardPile.addCard(item)
        print("===Battle END===")
            
        
class Monster:
    def __init__(self, name, hp, atk, xp=0, drop=""):
        self.name = name
        self.atk = atk
        self.maxhp = hp
        self.hp = hp
        self.xp = xp
        self.drop=drop
        
        self.dead = False
    
    def showInfo(self):
        print("{} emerged!".format(self.name))
        print("HP: {}/{}, ATK: {}".format(self.hp, self.maxhp, self.atk))
        
    def showHp(self):
        print("System: {}'s HP: {}/{}".format(self.name, self.hp, self.maxhp))
    
    def isDead(self):
        return self.dead
    
    def getXp(self):
        return self.xp
    
    def getDrop(self):
        # TODO: Implement 
        if drop != "":
            dropItem = drop[self.drop]
            rate = random.random()
            if rate <= dropItem[1]:
                return dropItem[0]
            else:
                return -1
        
    def reduceHp(self, amount):
        if not self.dead:
            self.hp -= amount
            print("Monster[{}]: receive {} damage. HP: {}/{}".format(self.name, amount, self.hp, self.maxhp))
            if self.hp <= 0:
                print("Monster[{}]: Dead".format(self.name))
                self.dead = True
    
    def attack(self, player):
        if not self.dead:
            print("Monster[{}]: attack {} damage.".format(self.name, self.atk))
            player.getHit(self.atk)
    
    def getName(self):
        return self.name
    
class Player:
    def __init__(self):
        self.name = "Player"
        self.maxhp = 100
        self.maxmp = 10
        self.hp = 100
        self.mp = 10
        self.str = 1
        self.int = 1
        self.agi = 1
        self.luck = 1
        self.speed = 1
        
        self.level = 1
        self.exp = 0
        self.gold = 0
        
        # Mode
        self.defense = False
        
        # Debuff 
        self.stunt = 0 # turn
        self.poison = (0, 0) #turn, damage
        
        # Equipment
        self.weaponAtk = 0
        self.armourDef = 0
        self.armour = ""
        self.weapon = ""
        
        # Card Effect
        self.cardAtk = 0
        self.cardAtkPercent = 1.0
        self.cardDef = 0
        self.cardDefPercent = 1.0
        self.cardCrit = 0.0
        self.cardEva = 0.0
        
        # Flag
        self.gameOver = False
    
    def levelUp(self, exp):
        self.exp += exp
        print("System: get {} experience => {}/{} to next level ".format(exp, self.exp, xp[self.level]))
        if self.exp >= xp[self.level]:
            self.exp -= xp[self.level]
            print("System: Level up! from {} to {}".format(self.level, self.level+1))
            self.level += 1
            print("System: you get 3 attribute point")
            point = 4
            addStr = 0
            addInt = 0
            addAgi = 0
            addLuck = 0
            addSpeed = 0
            while(point>0):
                print("System: assign attribute point to \n1: STR{}\n2: INT{}\n3: AGI{}\n4: LUCK{}\n5: SPEED{}".format(addStr*'+', addInt*'+', addAgi*'+', addLuck*'+', addSpeed*'+'))
                num = int(input("Choose (-1 to reset the assigned point): "))
                if num == 1:
                    addStr += 1
                elif num == 2:
                    addInt +=1
                elif num == 3:
                    addAgi += 1
                elif num == 4:
                    addLuck += 1
                elif num == 5:
                    addSpeed += 1
                elif num == -1:
                    point = 5
                    addStr = 0
                    addInt = 0
                    addAgi = 0
                    addLuck = 0
                    addSpeed = 0
                else:
                    print("System: Choose wrong number")
                    continue
                point -= 1
                if point == 0:
                    print("System: Confirm? \n1: STR{}\n2: INT{}\n3: AGI{}\n4: LUCK{}\n5: SPEED{}".format(addStr*'+', addInt*'+', addAgi*'+', addLuck*'+', addSpeed*'+'))
                    con = input("Type 0 to reset or else to confirm: ")
                    if con=='0':
                        point = 4
                        addStr = 0
                        addInt = 0
                        addAgi = 0
                        addLuck = 0
                        addSpeed = 0
                    else:
                        break
                    
            self.str += addStr
            self.int += addInt
            self.agi += addAgi
            self.luck += addLuck
            self.speed += addSpeed
            print("Player Stats: {}".format(self.getAttr()))
            print("{}".format(self.getStats()))
    
    def isDead(self):
        return self.gameOver
        
    def addCardEffect(self, heal=0, recover=0, cardAtk=0, cardAtkPercent=0, cardDef=0, cardDefPercent=0, cardCrit=0, cardEva=0):
        self.cardAtk += cardAtk
        self.cardAtkPercent += cardAtkPercent
        self.cardDef += cardDef
        self.cardDefPercent += cardDefPercent
        self.cardCrit += cardCrit
        self.cardEva += cardEva
        if heal != 0: self.heal(heal)
        if recover !=0: self.recover(recover)
    
    def resetAttackCard(self):
        self.cardAtk = 0
        self.cardAtkPercent = 1.0
        self.cardDef = 0
        self.cardDefPercent = 1.0
        self.cardCrit = 0.0
        self.cardEva = 0.0

    def getAttr(self):
        attrs = dict()
        attrs['STR'] = self.str
        attrs['INT'] = self.int
        attrs['AGI'] = self.agi
        attrs['LUCK'] = self.luck
        attrs['SPEED'] = self.speed
        return attrs
    
    def getStats(self):
        stats = dict()
        stats['MaxHP'] = self.maxhp
        stats['MaxMP'] = self.maxmp
        stats['HP'] = self.hp
        stats['MP'] = self.mp
        stats['ATK'] = math.ceil((math.ceil(self.str*0.4+self.weaponAtk)+self.cardAtk)*self.cardAtkPercent)
        stats['DEF'] = math.ceil((math.ceil(self.str*0.3+self.armourDef)+self.cardDef)*self.cardDefPercent)
        stats['CRIT'] = self.agi*0.007+self.luck*0.002+0.05+self.cardCrit
        stats['EVA'] = self.agi*0.001+self.speed*0.007+0.05+self.cardEva
        
        return stats
    
    def equip(self, equipmentType, name, attr):
        print("Player: equip {}, with attribute {}".format(name, attr))
        if equipmentType == "Armour":
            self.armour =  name
            self.armourDef = attr
        elif equipmentType == "Weapon":
            self.weapon = name
            self.weaponAtk = attr
        else:
            print("ERROR: equipmentType not match [Armour, Weapon]")
            raise
        
    def rest(self):
        print("Player: rest activated mp+5, MP: {}/{}".format(self.mp, self.maxmp))
        self.mp += 5
        if self.mp > self.maxmp:
            self.mp = self.maxmp
        # end turn
            
    def defend(self):
        stats = self.getStats()
        print("Player: defense activated, DEF: {}".format(stats['DEF']))
        self.defense = True
        # end turn
    
    def showHpMp(self):
        print("System: Player's HP: {}/{}, MP: {}/{}".format(self.hp, self.maxhp, self.mp, self.maxmp))
    
    def getMp(self):
        return self.mp
    
    def useMp(self, amount):
        if self.mp >= amount:
            self.mp -= amount
            return True
        return False
        
    def initTurn(self):
        self.defense = False
        # Reset card effect
        self.cardAtk = 0
        self.cardAtkPercent = 1.0
        self.cardDef = 0
        self.cardDefPercent = 1.0
        self.cardCrit = 0.0
        self.cardEva = 0.0
        # Reset Debuff 
        self.stunt = 0 # turn
        self.poison = (0, 0) #turn, damage
        
        self.mp = self.mp+4 if self.mp+4 <= self.maxmp else self.maxmp
        
    def getHit(self,pureDamage, physical = True):
        # return amount of damage
        stats = self.getStats()
        def reduceHp(amount):
            self.hp -= amount
            print("Player: receive {} damage, HP: {}/{}".format(amount, self.hp, self.maxhp))
            if self.hp <=0:
                self.gameOver = True
                print("Player: Dead!")
        def evade():
            return random.random() <= stats['EVA']
        if physical:
            if self.defense: 
                if evade():
                    print("Player: evaded!")
                    return 0
                reduceHp(max(1, pureDamage - stats['DEF']))
            else:
                if evade(): 
                    print("Player: evaded!")
                    return 0
                reduceHp(pureDamage) 
        else:
            reduceHp(pureDamage)
    
    def heal(self, amount):
        self.hp = min(self.hp+amount,self.maxhp)
        print("Player: heal {} hp, HP: {}/{}".format(amount, self.hp, self.maxhp))
    
    def recover(self, amount):
        self.mp = min(self.mp+amount,self.maxmp)
        print("Player: recover {} mp, MP: {}/{}".format(amount, self.mp, self.maxmp))
        
    def attack(self, monster):
        stats = self.getStats()
        if self.isCritical():
            print("Player: Landing a critical hit!!! {} with damage of {}".format(monster.getName(), stats['ATK']*2))
            monster.reduceHp(stats['ATK']*2)
            return
        print("Player: attack {} with damage of {}".format(monster.getName(), stats['ATK']))
        monster.reduceHp(stats['ATK'])
        
    def isCritical(self):
        stats = self.getStats()
        rate = random.random()
        if rate <= stats['CRIT']:
            return True
        return False

if __name__ == '__main__':
  print('''
# Created by Satasuk Viparksinlapin
#
# tl;dr
# this program is for create a card pile to draw and discard card
#
#
# Tutorial
# 1. create a game by 
#   game = Cardpile(warrior) # or rogue
# 2. let's start the game by call these method in every turn
#   game.init() # draw a card
#   game.use(int: cardID) # use a card
# 3. you may call 'game.draw()' if you have to
# ===================================ENJOY===================================

''')
