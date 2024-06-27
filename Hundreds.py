#Hundreds v1.3
#A card game by Cooper Sitaras
#Digital adaptation by Cooper Sitaras

import random as r
from time import sleep

class Player:
    chosenNames = []
    def __init__(self,lives,isPlayer = False):  #isPlayer: is the human player
        self.__handSize = 0
        self.__lives = lives
        self.__hand = []
        self.__oor = False  #Out of Round
        self.__oog = False  #Out of Game
        self.__isPlayer = isPlayer
        self.__dCount = 2   # of cards that must be discarded at the end of this round
        if self.__isPlayer == True:
            self.__name = 'you'
        else:
            validName = False
            names = ['Alex','Alice','Amber','Cameron','Clint','Eddie','Fred','Josh','Matthew','May','Rachel','Rosa','Ryan']
            #Picks a name at random for the CPU. There can't be more than 1 of each name
            #in a game.
            while validName == False:
                choice = r.randint(0,len(names)-1)
                if choice not in self.chosenNames:
                    validName = True
                    self.chosenNames.append(choice)
            self.__name = names[choice]

    def lives(self):
        return self.__lives
    def hand(self):
        return self.__hand
    def oor(self):
        return self.__oor
    def oog(self):
        return self.__oog
    def isPlayer(self):
        return self.__isPlayer
    def name(self):
        return self.__name
    def dCount(self):
        return self.__dCount

    def setHandSize(self,no):
        self.__handSize = no
    def handSizeDown(self):
        self.__handSize -= 1

    def draw(self,doText = True):
        #Makes the given player draw a card.
        card = deck.pop(0)
        if (self.__isPlayer == True) and (doText == True):
            scroll((f"You draw a {card.name()}.",),b=False)
        elif (self.__isPlayer == False) and (doText == True):
            scroll((f"{self.__name} draws.",),b=False)
        self.__hand.append(card)

    def play(self,card):
        #Makes the given player play the card 'card'
        played = False
        turnUsed = card.doCard(self.__isPlayer)
        newHand = []
        if turnUsed:
            #If the chosen card can be played at the moment:
            for i in self.__hand:
                if (i.name() == card.name()) and (played == False):
                    #If the name of the played card matches this card in their hand,
                    #and they haven't already played 1 card,don't include it in their
                    #updated hand
                    played = True
                else:
                    #Otherwise, include it
                    newHand.append(i)
            self.__hand = newHand
        #Put the played card back in the deck
        deck.append(card)
        return turnUsed

    def discard(self,cardNo):
        #Makes the player discard 'cardNo' cards
        discarded = False
        if self.__isPlayer == True:
            #Player discard
            prompt = ''
            for i in self.__hand:
                prompt += i.name() + '   '
            scroll((f"Select a card to discard. ({cardNo} left to discard)",
                    prompt),p=False,b=False)
            pin = input().lower()
            validCard = False
            while validCard == False:
                for i in self.__hand:
                    if i.name().lower() == pin:
                        index = self.__hand.index(i)
                        validCard = True
                if validCard == False:
                    if i.name() in ['1','2','3','4','5','6','7','8','9','10','-10','Double','Pass','Reverse','99']:
                        scroll(("You don't have that card in your hand.",))
                    else:
                        scroll(("Input not recognized.",))
            newHand = []
            for i in self.__hand:
                if (i.name() == pin) and (discarded == False):
                    discarded = True
                elif (i.name() == pin) and (discarded == True):
                    newHand.append(i)
                else:
                    newHand.append(i)
            self.__hand = newHand
            cardNo -= 1
            while cardNo > 0:
                discarded = False
                prompt = ''
                for i in self.__hand:
                    prompt += i.name() + '   '
                scroll((f"Select another card to discard. ({cardNo} left to discard)",
                        prompt),p=False,b=False)
                pin = input().lower()
                validCard = False
                while validCard == False:
                    for i in self.__hand:
                        if i.name().lower() == pin:
                            index = self.__hand.index(i)
                            validCard = True
                    if validCard == False:
                        if i.name() in ['1','2','3','4','5','6','7','8','9','10','-10','Double','Pass','Reverse','99']:
                            scroll(("You don't have that card in your hand.",))
                        else:
                            scroll(("Input not recognized.",))
                newHand = []
                for i in self.__hand:
                    if (i.name() == pin) and (discarded == False):
                        discarded = True
                    elif (i.name() == pin) and (discarded == True):
                        newHand.append(i)
                    else:
                        newHand.append(i)
                discarded = False
                self.__hand = newHand
                cardNo -= 1
        else:
            #CPU discard
            while cardNo > 0:
                print("discarding 1 card...")
                values = [i.value() for i in self.__hand]
                index = values.index(max(values))
                newHand = [i for i in self.__hand if self.__hand.index(i) != index]
                cardNo -= 1
                self.__hand = newHand
                
    def canPlay(self):
        #Tests to see if the given player has any playable cards
        canPlay = False
        for i in self.__hand:
            if ((i.value() + stack) <= 99):
                canPlay = True
                break
        return canPlay

    def canPlayCards(self):
        #Returns a list of the indeces of all playable cards in the given
        #player's hand
        cPC = []
        for i in range(0,len(self.__hand)):
            if (self.__hand[i].value() + stack <= 99):
                cPC.append(i)
        return cPC

    def hasCard(self,card):
        #Tests to see if the given player has a card with name 'card' in
        #their hand
        hasCard = False
        for i in self.__hand:
            if i.name() == card:
                hasCard = True
                break
        return hasCard

    def isLosing(self):
        #Tests to see whether any player has more lives than itself
        lives = self.__lives
        maxLives = 0
        for i in game:
            if i.__lives > maxLives:
                maxLives = i.__lives
        if maxLives > lives:
            return True
        else:
            return False

    def outOfRound(self,isPlayer):
        #Removes the given player from the round and executes most
        #related processes
        if isPlayer:
            scroll(("You fold.",))
        else:
            scroll((f"{self.__name} folds.",))
        self.__lives -= 1
        if self.__lives == 0:
            self.__oog = True
        self.__oor = True
        self.__handSize -= 1

    def reset(self):
        #Adds the given player back to the round
        self.__oor = False

    def doTurn(self):
        #Determines whether to run playerTurn or oppTurn
        if self.__isPlayer == True:
            self.doPlayerTurn()
        elif self.__isPlayer == False:
            self.doOppTurn()
        if self.__oor == True:
            return False
        else:
            return True

    def doPlayerTurn(self):
        #Executes all actions relating to the player's turn
        global turns
        global nextTurns
        turnsTaken = 0
        scroll((f"It's your turn! The stack is {stack}.",),b=False)
        if turns != 1:
            scroll((f"You'll need to play {turns} cards.",),b=False)
        if self.__oor == False:
            for i in range(turns):
                self.draw(True)
        while (turnsTaken < turns):
            if self.canPlay() == False:
                if (turnsTaken != 0):
                    scroll(("You don't have any more playable cards.",))
                else:
                    scroll(("But you don't have any playable cards.",))
                self.outOfRound(True)
                self.__dCount = (turns-turnsTaken+1)
                break
            else:
                prompt = ''
                for i in self.__hand:
                    prompt += i.name() + '   '
                scroll(("What card will you play?",
                        prompt,
                        "Type 'fold' to give up for this round.",),p=False,b=False)
                pin = input().lower()
                if 'fold' in pin:
                    self.outOfRound(True)
                    self.__dCount = (turns-turnsTaken+1)
                    break
                if self.__oor == False:
                    for i in self.__hand:
                        if i.name().lower() == pin:
                            if self.play(i):
                                turnsTaken += 1
                                match i.name():
                                    case '8':
                                        scroll(("You play an 8.",
                                                f"The stack is now {stack}."),b=False)
                                    case _:
                                        scroll((f"You play a {i.name()}.",
                                                f"The stack is now {stack}."),b=False)
                                break
                            else:
                                break
                    else:
                        if i.name() in ['1','2','3','4','5','6','7','8','9','10','-10','Double','Pass','Reverse','99']:
                            scroll(("You don't have that card in your hand.",))
                        else:
                            scroll(("Input not recognized.",))
        print()
        turns = nextTurns
        nextTurns = 1
        return self.__oor

    def doOppTurn(self):
        #Executes all actions relating to the given CPU's turn
        #Also contains the algorithm that determines which card
        #they will play
        global turns
        global nextTurns
        handSize = len(self.__hand)
        turnsTaken = 0
        scroll((f"It's {self.__name}'s turn!",),b=False)
        if turns != 1:
            scroll((f"They must play {turns} times.",),b=False)
        if self.__oor == False:
            for i in range(turns):
                self.draw(True)
        turnUsed = False
        while (turnsTaken < turns) or (turnUsed == False):
            turnUsed = False
            if self.canPlay() == False:
                self.outOfRound(False)
                self.__dCount = (turns-turnsTaken+1)
                break
            else:
                if (len(self.canPlayCards()) < (turns-turnsTaken)) and (not self.hasCard('-10')):
                    self.outOfRound(False)
                    self.__dCount = (turns-turnsTaken+1)
                    break
                powCount = 0
                index = 0
                for i in self.__hand:
                    if i.power() == True:
                        powCount += 1
                powPcnt = powCount/len(self.__hand)
                pChoice = r.random()    #What kind of play they'll make
                cChoice = r.randint(0,len(self.__hand)-1)   #Index of the card they'll play, if relevant
                values = [i.value() for i in self.__hand]
                if powPcnt == 1:
                    #If they have only power cards, they'll either choose randomly,
                    #fold with a good hand, or play their best card
                    if (pChoice < 0.2):
                        index = cChoice
                    elif (pChoice < 0.4) and (self.__lives > 1) and self.hasCard('99') and (not self.isLosing()):
                        self.outOfRound(False)
                        self.__dCount = (turns-turnsTaken+1)
                        turnUsed = True
                        break
                    elif (pChoice < 0.6) and (self.__lives > 1) and (not self.isLosing()):
                        self.outOfRound(False)
                        self.__dCount = (turns-turnsTaken+1)
                        turnUsed = True
                    else:
                        index = values.index(min(values))
                elif (0.75 <= powPcnt <= 1) and (stack >= 89):
                    #If they have mostly power cards, they'll either choose randomly,
                    #fold with a good hand, play a 99, or play a power card
                    if (pChoice < 0.1):
                        index = r.choice(self.canPlayCards())
                    elif (pChoice < 0.2) and (self.__lives > 1) and self.hasCard('99') and (not self.isLosing()):
                        self.outOfRound(False)
                        self.__dCount = (turns-turnsTaken+1)
                        turnUsed = True
                    elif (pChoice < 0.3) and (self.__lives >1) and (not self.isLosing()):
                        self.outOfRound(False)
                        self.__dCount = (turns-turnsTaken+1)
                        turnUsed = True
                    elif (pChoice < 0.9):
                        if self.hasCard('99') and (pChoice < 0.5):
                            index = values.index(-5)
                        elif (pChoice < 0.5):
                            pCard = False
                            while pCard == False:
                                index = r.randint(0,len(self.__hand)-1)
                                pCard = self.__hand[index].power()
                        else:
                            pCard = True
                            while (pCard == True) and (self.__hand[index].value() + stack <= 99):
                                index = r.randint(0,len(self.__hand)-1)
                                pCard = self.__hand[index].power()
                    else:
                        index = r.choice(self.canPlayCards())
                elif (79 <= stack <= 99):
                    #play a random power card, or play a random card
                    if (powPcnt != 0) and (pChoice < 0.1):
                        pCard = False
                        while pCard == False:
                            index = r.randint(0,len(self.__hand)-1)
                            pCard = self.__hand[index].power()
                    else:
                        index = r.choice(self.canPlayCards())
                else:
                    #play their largest value card, or play a random card
                    if (pChoice < 0.8):
                        index = values.index(max(values))
                    else:
                        index = r.choice(self.canPlayCards())
            turnsTaken += 1
            if (not self.__oor) and (self.__hand[index].value() + stack <= 99):
                match self.__hand[index].name():
                    case '8':
                        scroll((f"{self.__name} plays an 8.",),b=False)
                    case _:
                        scroll((f"{self.__name} plays a {self.__hand[index].name()}.",),b=False)
                turnUsed = self.play(self.__hand[index])
                scroll((f"The stack is now {stack}.",),b=False)
        while (len(self.__hand) < self.__handSize) and (self.__oor == False):
            self.draw(False)
        while (len(self.__hand) > self.__handSize) and (self.__oor == False):
            self.discard(1)
##        if len(self.__hand) > handSize:
##            self.discard(len(self.__hand)-handSize)
##        elif len(self.__hand) < handSize:
##            self.draw(False)
        turns = nextTurns
        nextTurns = 1
        print()
        return self.__oor

    def __str__(self):
        return f"{self.__name}:\n\
Lives: {self.__lives}\n\
# of Cards: {len(self.__hand)}\n\
OOR?: {self.__oor} OOG?: {self.__oog}\n\
Discard Count: {self.__dCount}"
#-----END PLAYER CLASS----------------------------------------------------------


class Card:
    def __init__(self,name):
        match name:
            #cardType is the name of the card
            #value is the value of the card
                #straightforward for number cards
                #power cards have negative values, bigger negative
                    #numbers means more powerful (to me, at least)
            #power is whether the card is a power card
            case 1:
                self.__cardType = '1'
                self.__value = 1
                self.__power = False
            case 2:
                self.__cardType = '2'
                self.__value = 2
                self.__power = False
            case 3:
                self.__cardType = '3'
                self.__value = 3
                self.__power = False
            case 4:
                self.__cardType = '4'
                self.__value = 4
                self.__power = False
            case 5:
                self.__cardType = '5'
                self.__value = 5
                self.__power = False
            case 6:
                self.__cardType = '6'
                self.__value = 6
                self.__power = False
            case 7:
                self.__cardType = '7'
                self.__value = 7
                self.__power = False
            case 8:
                self.__cardType = '8'
                self.__value = 8
                self.__power = False
            case 9:
                self.__cardType = '9'
                self.__value = 9
                self.__power = False
            case 10:
                self.__cardType = '10'
                self.__value = 10
                self.__power = False
            case -10:
                self.__cardType = '-10'
                self.__value = -1
                self.__power = True
            case 'D':
                self.__cardType = 'Double'
                self.__value = -4
                self.__power = True
            case 'P':
                self.__cardType = 'Pass'
                self.__value = -2
                self.__power = True
            case 'R':
                self.__cardType = 'Reverse'
                self.__value = -3
                self.__power = True
            case 99:
                self.__cardType = '99'
                self.__value = -5
                self.__power = True

    def name(self):
        return self.__cardType
    def value(self):
        return self.__value
    def power(self):
        return self.__power

    def doCard(self,isPlayer):
        #executes the effect(s) of the card, whichever card it may be
        global stack
        global nextTurns
        global game
        global isReversed
        if (self.__value + stack) <= 99:
            match self.__cardType:
                case '1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'|'10':
                    stack += self.__value
                case '-10':
                    stack -= 10
                case 'Double':
                    nextTurns *= 2
                case 'Pass':
                    pass
                case 'Reverse':
                    isReversed = not isReversed
                    pass
                case '99':
                    stack = 99
            turnUsed = True
        elif isPlayer == True:
            scroll(("The stack is too high to play that card right now.",))
            turnUsed = False
        else:
            turnUsed = False
        return turnUsed
#-----END CARD CLASS------------------------------------------------------------

#-----END ALL CLASSES-----------------------------------------------------------

game = []
deck = []
stack = 0
turns = 1
nextTurns = 1
turnNo = 0
isReversed = False

def scroll(text,p=True,b=True):
    lines = 0
    if b == True:
        sleep(0.5)
        print()
    for i in text:
        print(i)
        sleep(0.1)
        lines += 1
    if p == True:
        sleep(lines * 0.5)

def gameStart(playerCount,lives,noCards):
    #executes all processes related to the beginning of a new game
    global game
    Player.chosenNames = []
    game = []
    for i in range(playerCount-1):
        game.append(Player(lives))
    game.append(Player(lives,True))
    cards = [1,2,3,4,5,6,7,8,9,10,-10,'D','P','R',99]
    for i in range(4):
        for j in range(15):
            deck.append(Card(cards[j]))
    r.shuffle(deck)
    r.shuffle(game)
    for i in range(len(game)):
        for j in range(noCards):
            game[i].draw(False)
        game[i].setHandSize(noCards)
    scroll((f"The stack is {stack}.",),b=False)

def roundStart(game):
    #executes all processes related to the beginning of a new round
    for i in game:
        if i.lives() == 0:
            if i.isPlayer() == True:
                scroll((f"You're out!",))
            else:
                scroll((f"{i.name()} is out!",))
    newGame = [i for i in game if i.lives() > 0]
    return newGame

def printNames(game):
    #used for echo printing
    for i in game:
        print(i.name(),end=' ')
    print()

def printGame(game):
    #used for echo printing
    for i in game:
        print(i)

def hundreds():
    #controls the flow of the game as a whole
    global game
    global stack
    winner = ''
    turnNo = 0
    gamePlay = True
    gameNo = 1
    while gamePlay == True:
        #controls the flow of the game
        #printGame(game)
        playersOut = 0
        game = roundStart(game)
#-----CHANGE THIS FOR TESTING---------------------------------------------------
        stack = 0
#-------------------------------------------------------------------------------
        playerAlive = False
        for i in game:
            if (i.isPlayer() and (i.oog == False)):
                playerAlive = True
        if (len(game) == 1):
            winner = game[0].name()
            gamePlay = False
        else:
            if gameNo > 1:
                for i in game:
                    if i.oor() == True:
                        i.discard(i.dCount())
                        i.reset()
            for i in game:
                prompt = ''
                if i.name() == 'you':
                    prompt += 'You have '
                else:
                    prompt += i.name() + ' has '
                if i.lives() == 1:
                    prompt += '1 life and '
                else:
                    prompt += str(i.lives()) + ' lives and '
                if len(i.hand()) == 1:
                    prompt += '1 card remaining.'
                else:
                    prompt += str(len(i.hand())) + ' cards remaining.'
                scroll((prompt,),b=False)
            print()
            roundPlay = True
            while roundPlay == True:
                #controls the flow of each round
                playerNo = turnNo % len(game)
                if turnNo % 10 == 0:
                    r.shuffle(deck)
                if (game[playerNo].oor() == False) and (game[playerNo].lives() > 0):
                    if game[playerNo].doTurn() == False:
                        playersOut += 1
                if playersOut == len(game)-1:
                    roundPlay = False
                if isReversed == False:
                    turnNo += 1
                else:
                    turnNo -= 1
                if turnNo == 0:
                    turnNo = 10*len(game)
            for i in game:
                if i.oor() == False:
                    if i.name() == 'you':
                        scroll(("You win the round!",))
                    else:
                        scroll((f"{i.name()} wins the round!",))
            gameNo += 1
    if winner == 'you':
        scroll(("You won the game!",))
        return True
    elif winner == '':
        scroll(("An unexpected error has occurred while ending the game.",))
        pass
    else:
        scroll((f"{winner} won the game!",))
        return False

def main(playerCount,lives,noCards):
    #begins and ends the game as a whole
    gameStart(playerCount,lives,noCards)
    win = hundreds()
    return win

def mainer(playerCount = 4,lives = 3,noCards = 3):
    #controls everything related to beginning the game (the menu, basically)
    #if this module is being imported, launches directly into a normal game
    #otherwise, brings you to the main menu.
    if __name__ == "__main__":
        runProgram = True
        while runProgram == True:
            scroll(("Welcome to Hundreds!",
                    "Type 'play' to start a game,",
                    "Type 'info' to learn how to play,",
                    "Or type 'exit' to end the program."),p=False)
            pin = input().lower()
            if 'play' in pin:
                playMenu = True
                while playMenu == True:
                    scroll(("Choose your gamemode:",
                            "Normal: 4 players, 3 cards, 3 lives",
                            "Quick: 4 players, 3 cards, 1 life",
                            "Long: 4 players, 5 cards, 5 lives",
                            "Custom: choose the settings yourself.",
                            "Type 'back' to return to the main menu."),p=False)
                    pin = input().lower()
                    if 'back' in pin:
                        playMenu = False
                    elif 'normal' in pin:
                        playMenu = False
                        main(playerCount,lives,noCards)
                    elif 'quick' in pin:
                        playMenu = False
                        main(4,1,3)
                    elif 'long' in pin:
                        playMenu = False
                        main(4,5,5)
                    elif 'custom' in pin:
                        customMenu = True
                        pChosen = False
                        lChosen = False
                        cChosen = False
                        while (customMenu == True) and (pChosen == False):
                            scroll(("Choose the number of players (2-6):",
                                    "Type 'back' to return the game menu."),p=False)
                            pin = input().lower()
                            if 'back' in pin:
                                customMenu = False
                            else:
                                try:
                                    pin = int(pin)
                                except:
                                    scroll(("Please enter an integer.",))
                                else:
                                    if (pin < 2) or (pin > 6):
                                        scroll(("Number of players must be between 2 and 6.",))
                                    else:
                                        pCount = pin
                                        pChosen = True
                        while (customMenu == True) and (cChosen == False):
                            scroll(("Choose the number of cards each player will start with (1-5):",
                                    "Type 'back' to return to the game menu."),p=False)
                            pin = input().lower()
                            if 'back' in pin:
                                customMenu = False
                            else:
                                try:
                                    pin = int(pin)
                                except:
                                    scroll(("Please enter an integer.",))
                                else:
                                    if (pin < 1) or (pin > 5):
                                        scroll(("Number of cards must be between 1 and 5.",))
                                    else:
                                        cCount = pin
                                        cChosen = True
                        while (customMenu == True) and (lChosen == False):
                            scroll(("Choose the number of lives each player will start with:",
                                    "Type 'back' to return to the game menu."),p=False)
                            pin = input().lower()
                            if 'back' in pin:
                                customMenu = False
                            else:
                                try:
                                    pin = int(pin)
                                except:
                                    scroll(("Please enter an integer.",))
                                else:
                                    if (pin < 1) or (pin > cCount):
                                        scroll(("Number of lives must be greater than 0 and less than number of cards.",))
                                    else:
                                        lCount = pin
                                        lChosen = True
                        if customMenu == True:
                            main(pCount,lCount,cCount)
                            customMenu = False
            elif 'info' in pin:
                scroll((
            "Hundreds is a quick, strategic, and suspenseful card game fun for all ages!",
            "",
            "The Object of the Game:",
            "    The object of the game is to be the last one standing. If you can't avoid",
            "pushing the value of the discard pile over 99, you're out of the round!",
            "If the game has more than 1 life for each player, the losers of every round",
            "will permanently lose a card from their hand, reducing their options later.",
            "The last player with any cards left in their hand wins!",
            "",
            "Taking a Turn:",
            "    Each player's turn consists of drawing a card, then playing a card. The",
            "game then announces the sum of the values of all cards in the discard pile",
            "(referred to as 'the stack' from here on), and play proceeds clockwise to the",
            "next player. Most cards' values are their face values, however some cards have",
            "special abilities.",
            "    A player may also use their turn to fold. See the 'Ending the Round'",
            "section for more information on folding.",
            "",
            "The Deck:",
            "    The 60 cards in a Hundreds deck have a variety of effects. Here's what each",
            "card does.",
            "1-10:    Act as their face value. When played, they raise the stack by that",
            "         amount.",
            "Double:  Does not affect the stack. Instead, the next player must draw two and",
            "         then play two cards on their turn.",
            "Pass:    Does not affect the stack. It can be used as a free play, getting you",
            "         out of a tough spot. If you've been doubled, you'll still need to play",
            "         another card for your turn.",
            "Reverse: Does not affect the stack. Instead, it reverses the turn order. This",
            "         effect persists between rounds.",
            "99:      Instantly raises the stack to 99. It can still be played when the stack",
            "         is 99.",
            "",
            "Ending the Round:",
            "    When you can't keep the stack from going over 99, you're out of the round,",
            "and will automatically fold. The round will continue until all but 1 player has",
            "folded. At the end of the round, if players have more than 1 life, every",
            "eliminated player will choose 2 cards from their hand to discard - for a net -1,",
            "since they would have drawn before folding - before the next round starts. This",
            "also means that if you were doubled and unable to complete your turn, you'll",
            "have to discard more than 2 cards.",
            "    A player may also choose to fold at any point, even if they have a card they",
            "could have played. This may be a strategic move to save a good hand for later.",
            "",
            "New Rounds:",
            "    When starting a new round, every loser of the last round resumes play with",
            "the same hand they had before, and the stack is reset to 0. Play resumes as",
            "normal from the player who would have played after the winner, taking any",
            "reverses into account.",
            "",
            "Ending the Game:",
            "    When a player is forced to discard their last card, they're out of the game",
            "for good. The last player with cards left wins!"),p=False)
            elif 'exit' in pin:
                scroll(("Thank you for playing!",
                        "",
                        "Shutting down."))
                runProgram = False
            else:
                scroll(("Input not recognized.",))
    else:
        main(4,3,3)

mainer()
