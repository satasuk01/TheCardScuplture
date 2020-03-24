#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 14:27:42 2020

@author: zeze
"""
import time
from libs import GameSystem as GS
from libs import Card
import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def randomMonster(hprange, atkrange, xprange, droprange=[0,3]):
    hp = random.randint(hprange[0],hprange[1])   
    atk = random.randint(atkrange[0],atkrange[1]) 
    xp = random.randint(xprange[0],xprange[1]) 
    drop = random.randint(droprange[0],droprange[1])
    return GS.Monster(randomString(),hp,atk,xp,drop)

def getMonsters(n,hprange, atkrange, xprange, droprange=[0,3]):
    monsters = []
    for i in range(n):
        monsters.append(randomMonster(hprange, atkrange, xprange, droprange=[0,3]))
    return monsters

if __name__ == '__main__':
    
    player = GS.Player()
#    monsters = [
#            GS.Monster('Slime', 10, 4, 10, 0),
#            GS.Monster('Slime', 10, 4, 10, 0),
#            GS.Monster('Slime Lv.2', 15, 5, 15, 1),
#            GS.Monster('Slime Lv.2', 15, 5, 15, 1),
#            GS.Monster('Skeleton', 30, 5, 15, 1),
#            GS.Monster('Bandit', 30, 7, 40),
#            ]
    monsters = getMonsters(7,[5,20],[5,9],[10,50])
    cardSystem = Card.Cardpile(player, Card.starter)
    for monster in monsters:
        cardSystem.addMonster(monster)
        system = GS.System(player, monster, cardSystem)
        # GAME
        system.battle()

    print("Game testing is done!")
    input()
    
