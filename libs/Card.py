import random
import math

starter = [0,0,0,0,5,5,5,2,2,3,1,1]
#rogue = [1,1,1,1,6,6,7,7,8,4]
cardTypes = ["Attack", "Defense", "Effect", "Item"]
cards = {
            0: {
                    "ID": 0,
                    "name": "Slay",
                    "cardType": "Attack",
                    "mpCost": 2,
                    "props": {"cardAtk":1, "chain":1},
                    "desc": "Atk. +1  at an enemy, Chain Atk +1",
                },
            1: {
                    "ID": 1,
                    "name": "Small Potion",
                    "cardType": "Item",
                    "mpCost": 0,
                    "props": {"heal":10},
                    "desc": "recovery 10 hp",
                },        
            2: {
                    "ID": 2,
                    "name": "Bash",
                    "cardType": "Attack",
                    "mpCost": 2,
                    "props": {"cardAtk":3},
                    "desc": "Atk. +3  at an enemy",
                },
            3: {
                    "ID": 3,
                    "name": "Sword Dance",
                    "cardType": "Attack",
                    "mpCost": 6,
                    "props": {"cardAtk":10},
                    "desc": "Atk. +10  at an enemy",
                },
            4: {
                    "ID": 4,
                    "name": "Focus",
                    "cardType": "Effect",
                    "mpCost": 3,
                    "props": {"cardCrit":0.5},
                    "desc": "Critical rate +50% next attack",
                },
            5: {
                    "ID": 5,
                    "name": "Guard",
                    "cardType": "Defense",
                    "mpCost": 1,
                    "props": {"cardDef":3},
                    "desc": "Def. +3",
                },
            6: {
                    "ID": 6,
                    "name": "Evade",
                    "cardType": "Effect",
                    "mpCost": 2,
                    "props": {"cardEva":0.3},
                    "desc": "Evasion +30% until the next turn.",
                },
            7: {
                    "ID": 7,
                    "name": "Back Stab",
                    "cardType": "Attack",
                    "mpCost": 5,
                    "props": {"cardATK":8, "cardCrit":0.2},
                    "desc": "Atk. +8  at an enemy with +20% critical chance",
                },
        }
class Card:
    def __init__(self, ID, name, cardType, mpCost, props, desc=""):
        self.name = name
        self.cardType = cardType
        self.cost = mpCost
        self.props = props
        self.desc = desc
        self.id = ID
        
    def use(self, player, monster, lastUsed):
        if not player.useMp(self.cost):
            print("System: mp not enough. require {} but have {}".format(self.cost, player.getMp()))
            return False
        if self.cardType == "Attack":
            atk = self.props['cardAtk']
            if "chain" in self.props:
                if lastUsed == self.id: atk += self.props['chain'] 
            player.addCardEffect(cardAtk=atk) # cardAtk and chain
            player.attack(monster)
            player.resetAttackCard()
        if self.cardType == "Defense":
            player.addCardEffect(cardDef=self.props['cardDef'])
            player.defend()
        if self.cardType == "Effect":
            player.addCardEffect(**self.props)
        if self.cardType == "Item":
            player.addCardEffect(**self.props)
        return True
    
    def getInfo(self):
        info = '''{}: {} type: {} cost: {} desc: {}'''.format(self.id,self.name, self.cardType, self.cost, self.desc)
        return info
    def getType(self):
        return self.cardType
    
class Cardpile:
  def __init__(self, player, cardIds):
    self.player = player
    self.monster = ""
    self.cardpile = cardIds[:] # drawable pile
    self.discardpile = [] # discard pile
    self.onhand = []
    self.turn = 0
    self.lastUse = -1 # id of the last used card
    
  def resetOnhand(self, ncards=6):
      self.discardpile += self.onhand
      self.onhand = []
      while(len(self.onhand)< ncards):
          self.onhand.append(self.draw())
      
      
  def shuffle(self):
    if(len(self.cardpile)==0):
      self.cardpile = self.discardpile
      self.discardpile = []
    new = self.cardpile
    random.shuffle(new)
    self.cardpile = new
#    print('shuffled')
    
  def draw(self):
    if(len(self.cardpile)==0):
#      print("no card left")
      self.shuffle()
    drawedCard = self.cardpile.pop()
    return drawedCard

  # ============== Callable =====================
  def getLenOnhand(self):
      return len(self.onhand)
      
  def showCard(self):
      for ID in self.onhand:
          print(Card(**cards[ID]).getInfo())
          
  def init(self, ncards = 6): # call this every turn
    self.turn += 1
    while(len(self.onhand)< ncards):
      self.onhand.append(self.draw())

  def addMonster(self, monster):
      self.monster = monster
      
  def addCard(self, card):
      self.cardpile += [card]
      print("System: get card {}".format(Card(**cards[card]).getInfo()))
      
  def use(self, cardid):
    cid = int(cardid)
    if not (cid in self.onhand):
      print("System: no {} on hand".format(cid))
#      print('on hand: {}'.format(self.onhand))
      return False
    else:
      isUsed = Card(**cards[cid]).use(self.player, self.monster, self.lastUse)
      if not isUsed:
          return False
      self.onhand.remove(cid)
      if Card(**cards[cid]).getType() != "Item": # scrape card if it is Item card
          self.discardpile.append(cid)
      self.lastUse = cid
    return True
    print('on hand: {}'.format(self.onhand))
    print('discard pile: {}'.format(self.discardpile))
    print('card pile left: {}'.format(len(self.cardpile)))


      