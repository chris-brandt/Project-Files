from random import randrange, uniform, choice, shuffle
import random

#defines the player class
class Table(object):
    def __init__(self):
        self.pot = 0
        self.cards = []
        self.deck = genDeck()
        self.raises = []
        self.amountdown = 0
    def __str__(self):
        string = ""
        for i in range(len(self.cards)):
            string += "["+decode(self.cards[i])+"]"
        return string

    def addCard(self):
        self.cards.append(self.deck.pop())

#defines the player class
class Player(object):
    def __init__(self, number, chips):
        self.ingame = True
        self.number = number
        self.chips = chips
        self.hand = []
        self.printhand = ""
        self.amountdown = 0
        self.bigblind = False
        self.smallblind = False
    def __str__(self):
        return ("Player%d" % self.number)

    def addCard(self, card):
        self.hand.append(card)
        self.printhand += "["+decode(card)+"]"

    def removeHand(self):
        return_list = self.hand
        self.hand = []
        return return_list

#checks if there was an allin scenario
def allIn(players):
    players_in = playersIn(True, players)
    diag = 0
    for i in range(len(players_in)):
        if players[i].chips != 0:
            diag += 1
    if diag == 0:
        diag = True
    else:
        diag = False
    return diag

#rotates the blinds
def blindRotate(players):
    if players[len(players)-1].bigblind:
        players[0].bigblind = True
        players[len(players) - 1].bigblind = False
        players[len(players)-1].smallblind = True
        players[len(players)-2].smallblind = False
    elif players[0].bigblind:
        players[0].bigblind = False
        players[1].bigblind = True
        players[len(players)-1].smallblind = False
        players[0].smallblind = True
        players[len(players)-1].smallblind = False
        players[0].smallblind = True
    else:
        index = 0
        for i in range(len(players)):
            if players[i].bigblind:
                index = i
        players[index].bigblind = False
        players[index+1].bigblind = True
        players[index-1].smallblind = False
        players[index].smallblind = True

#runs a computer's turn
def computerTurn(players, table, index):
    current_raise = table.amountdown - players[index].amountdown
    # | 1 - Call/Check | 2 - Fold | 3 - Raise |
    if current_raise == 0:
        choice = intInput("| (1) - Check | (2) - Raise | ", "! need an integer 1-2 !", 0, 3)
        if choice == 2:
            choice = 3
    #if there is a raise less than an allin
    elif current_raise > 0 and current_raise < players[index].chips:
        choice = intInput("| (1) - Call %d | (2) - Fold | (3) - Raise | " % current_raise, "! need an integer 1-3 !", 0, 4)
    #if there is an allin raise
    else:
        current_raise = current_raise - (players[index].chips - current_raise)
        choice = intInput("! (1) - All-In ! | (2) - Fold | ", "! need an integer 1-2 !", 0, 3)

    if choice == 1:
        players[index].chips -= current_raise
        players[index].amountdown += current_raise
        table.pot += current_raise
    elif choice == 2:
        players[index].ingame = False
    else:
        print()
        raise_input = 0
        raise_input = intInput("How much would you like to raise? ", "! need an integer 1-%d !" % (players[0].chips - current_raise), 0, (players[index].chips + 1) - current_raise)
        current_raise += raise_input
        players[index].chips -= current_raise
        players[index].amountdown += current_raise
        table.pot += current_raise
        table.amountdown += raise_input
        print()
    return

    return

#turns list elements to cards shown to the user
def decode(card):
    number = card[0]
    suit = card[1]
    if number < 11:
        if suit == 1:
            card = "%d♠" % number
        elif suit == 2:
            card = "%d♣" % number
        elif suit == 3:
            card = "%d♦" % number
        elif suit == 4:
            card = "%d♥" % number
    elif number == 11:
        if suit == 1:
            card = "J♠"
        elif suit == 2:
            card = "J♣"
        elif suit == 3:
            card = "J♦"
        elif suit == 4:
            card = "J♥"
    elif number == 12:
        if suit == 1:
            card = "Q♠"
        elif suit == 2:
            card = "Q♣"
        elif suit == 3:
            card = "Q♦"
        elif suit == 4:
            card = "Q♥"
    elif number == 13:
        if suit == 1:
            card = "K♠"
        elif suit == 2:
            card = "K♣"
        elif suit == 3:
            card = "K♦"
        elif suit == 4:
            card = "K♥"
    else:
        if suit == 1:
            card = "A♠"
        elif suit == 2:
            card = "A♣"
        elif suit == 3:
            card = "A♦"
        elif suit == 4:
            card = "A♥"
    return card

#deals cards to players
def deal(players, table):
    for i in range(2):
        for j in range(len(players)):
            card = table.deck.pop(0)
            players[j].addCard(card)

#creates a shuffled deck
def genDeck():
    #initialize all of the numbers that would be in the deck
    # 11 - Jack | 12 - Queen | 13 - King | 14 - Ace
    numbers = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    #initialize the suits
    # 1 - spades | 2 - clubs | 3 - diamonds | 4 - hearts
    suits = [1,2,3,4]
    #initialize the deck
    deck = []
    #loop through each suit
    for i in range(4):
        #loop through all of the numbers
        for j in range(len(numbers)):
            #create a card from the current suit and number and add it to deck
            item = [numbers[j],suits[i]]
            deck.append(item)
    #shuffle the deck
    random.shuffle(deck)
    return deck

#starts a hand
def handStart(players, table, blindNum):
    deal(players, table)
    for i in range(len(players)):
        if players[i].bigblind:
            players[i].chips -= blindNum
            players[i].amountdown += blindNum
            table.pot += blindNum
            table.amountdown += blindNum
        if players[i].smallblind:
            players[i].chips -= int(blindNum/2)
            players[i].amountdown += int(blindNum/2)
            table.pot += int(blindNum/2)
    index = nextTurn(players)
    return index

#organizes the end of a hand
def handOver(players, table):
    handWinner(players, table)
    for i in range(len(players)):
        print(players[i].chips)
    i = 0
    while i < len(players):
        if players[i].chips == 0:
            players.pop(i)
        else:
            players[i].hand = []
            players[i].amountdown = 0
            players[i].printhand = ""
            players[i].ingame = True
            i += 1
    if len(players) > 1:
        blindRotate(players)
    return

#determines the winner of a hand
def handWinner(players, table):
    players_in = playersIn(True, players)
    value_list = []
    for i in range(len(players_in)):
        value_list.append(handValue(players_in[i].hand, table.cards))

    highest_hand = 0
    for i in range(len(value_list)):
        if value_list[i][0] > highest_hand:
            highest_hand = value_list[i][0]
    highest_hands = []

    for i in range(len(value_list)):
        if value_list[i][0] == highest_hand:
            highest_hands.append([i, value_list[i]])
    winner = 0
    if len(highest_hands) > 1:
        #compare multiple high cards
        if highest_hand == 0:
            handWinnerFunc(highest_hands, 6)

        #compare multiple pairs
        elif highest_hand == 1:
            handWinnerFunc(highest_hands, 5)

        #compare multiple two pairs
        elif highest_hand == 2:
            handWinnerFunc(highest_hands, 4)

        #compare multiple three of a kinds
        elif highest_hand == 3:
            handWinnerFunc(highest_hands, 4)

        #compare straights
        elif highest_hand == 4:
            handWinnerFunc(highest_hands, 2)

        #compare flushes
        elif highest_hand == 5:
            handWinnerFunc(highest_hands, 6)

        #compare full houses
        elif highest_hand == 6:
            handWinnerFunc(highest_hands, 3)

        #compare four of a kinds
        elif highest_hand == 7:
            handWinnerFunc(highest_hands, 3)

        #compare straight flushes
        else:
            handWinnerFunc(highest_hands, 2)

    chips = 0
    if len(highest_hands) > 1:
        chips = int(table.pot)/len(highest_hands)
        for i in range(len(highest_hands)):
            if highest_hands[0] == i:
                players_in[i].chips += chips
    else:
        players_in[highest_hands[0][0]].chips += table.pot
    return

#a simple function used by handWinner to get the highest hand(s) in a list
#of the same hand type
def handWinnerFunc(highest_hands, length):
    i = 1
    while i < length:
        highest = 0
        for j in range(len(highest_hands)):
            if highest_hands[j][1][i] > highest:
                highest = highest_hands[j][1][i]

        k = 0
        while k < len(highest_hands):
            if highest_hands[k][1][i] < highest:
                highest_hands.pop(k)
            else:
                k += 1
        i += 1
    return

#assigns a value to a hand
#| 0 - high card | 1 - pair | 2 - two pair | 3 - three of a kind | 4 - straight
#| 5 - flush | 6 - full house | 7 - four of a kind | 8 - straight flush
def handValue(playerhand, tablecards):
    cardlist = playerhand + tablecards
    for i in range(len(cardlist) - 1):
        i += 1
        j = 0
        diag = 0
        while diag != 1:
            if cardlist[i][0] > cardlist[j][0]:
                j += 1
            else:
                diag = 1
        cardlist.insert(j, cardlist.pop(i))
    value = 0

    #create pair and triple list
    numberslist = []
    numberslist.append(cardlist[0][0])
    for i in range(len(cardlist)):
        for j in range(len(numberslist)):
            diag = 0
            if cardlist[i][0] == numberslist[j]:
                diag = 1
        if diag != 1:
            numberslist.append(cardlist[i][0])
    items = []
    for i in range(len(numberslist)):
        counter = 0
        for j in range(len(cardlist)):
            if numberslist[i] == cardlist[j][0]:
                counter += 1
        if counter == 3:
            items.append([3, numberslist[i]])
        elif counter == 2:
            items.append([2, numberslist[i]])

    #check pairs
    pairs = []
    for i in range(len(items)):
        if items[i][0] == 2:
            pairs.append(items[i][1])

    if len(pairs) == 1:
        value = [1, pairs[0]]
        max_num = 0
        numberslist_copy = numberslist.copy()
        while len(value) < 5:
            max_num = max(numberslist_copy)
            numberslist_copy.remove(max_num)
            if max_num != pairs[0]:
                value.append(max_num)


    elif len(pairs) > 1:
        value = [2, pairs[len(pairs) - 1], pairs[len(pairs) - 2]]
        i = 0
        max_num = 0
        numberslist_copy = numberslist.copy()
        while len(value) < 4:
            max_num = max(numberslist_copy)
            numberslist_copy.remove(max_num)
            if max_num == pairs[0] or max_num == pairs[1]:
                i += 1
            else:
                value.append(max_num)

    #check three of a kind
    for i in range(len(items)):
        if items[i][0] == 3:
            value = [3, items[i][1]]
    if type(value) == list and value[0] == 3:
        i = 0
        max_num = 0
        numberslist_copy = numberslist.copy()
        while len(value) < 4:
            max_num = max(numberslist_copy)
            numberslist_copy.remove(max_num)
            if max_num == value[1]:
                i += 1
            else:
                value.append(max_num)




    #check straight
    straight = True
    straight_number = 0
    startindex = 0
    for i in range(len(numberslist) - 4):
        for j in range(4):
            j += startindex
            if numberslist[j] + 1 != numberslist[j + 1]:
                straight = False
        if straight:
            straight_number = numberslist[i]
        startindex += 1
        straight = True
    if straight_number != 0:
        value = [4, straight_number]

    #check flush
    flush = 0
    counter = 0
    for i in range(4):
        i += 1
        for j in range(len(cardlist)):
            if cardlist[j][1] == i:
                counter += 1
        if counter >= 5:
            flush = i
        counter = 0
    if flush > 1:
        i = len(cardlist) - 1
        value = [5]
        while len(value) != 6:
            if cardlist[i][1] == flush:
                value.append(cardlist[i][0])
                i -= 1
            else:
                i -= 1


    #check full house
    triples = []
    doubles = []
    for i in range(len(items)):
        if items[i][0] == 3:
            triples.append(items[i][1])
        else:
            doubles.append(items[i][1])
    triple = 0
    if len(triples) == 2:
        value = [6, max(triples), min(triples)]
    elif len(triples) == 1 and len(doubles) == 2:
        value = [6, triples[0], max(doubles)]
    elif len(triples) == 1 and len(doubles) == 1:
        value = [6, triples[0], doubles[0]]


    #check four of a kind
    if len(numberslist) <= 4:
        for i in range(len(numberslist)):
            counter = 0
            for j in range(len(cardlist)):
                if numberslist[i] == cardlist[j][0]:
                    counter += 1
            if counter == 4:
                value = [7, numberslist[i]]
                i = 0
                max_num = 0
                numberslist_copy = numberslist.copy()
                while len(value) < 3:
                    max_num = max(numberslist_copy)
                    numberslist_copy.remove(max_num)
                    if max_num == value[1]:
                        i += 1
                    else:
                        value.append(max_num)


    #check straight flush
    #check and make flush
    flush = 0
    counter = 0
    for i in range(4):
        i += 1
        for j in range(len(cardlist)):
            if cardlist[j][1] == i:
                counter += 1
        if counter >= 5:
            flush = i
        counter = 0
    if flush > 0:
        flushlist = []
        for i in range(len(cardlist)):
            if cardlist[i][1] == flush:
                flushlist.append(cardlist[i])
    #now check straight
    if flush > 0:
        straightflush = True
        startindex = 0
        for i in range(len(flushlist) - 4):
            for i in range(4):
                i += startindex
                if flushlist[i][0] + 1 != flushlist[i + 1][0]:
                    straightflush = False
            if straightflush:
                value = [8, flushlist[startindex][0]]
            startindex += 1

    if value == 0:
        value = [0]
        i = 0
        max_num = 0
        numberslist_copy = numberslist.copy()
        while len(value) < 6:
            max_num = max(numberslist_copy)
            numberslist_copy.remove(max_num)
            value.append(max_num)

    return value

#gets an int input
def intInput(message1, message2, bottom, top):
    diag = 0
    while diag != 1:
        inputArg = input(message1)
        try:
            int(inputArg)
            inputArg = int(inputArg)
            if inputArg > bottom and inputArg < top:
                inputArg = int(inputArg)
                output = inputArg
                diag = 1
            else:
                print()
                print(message2)
                print()
        except:
            print()
            print(message2)
            print()
    return output

#figures out the player that should start a turn
def nextTurn(players):
    diag = 0
    index = -1
    while diag == 0:
        index += 1
        if players[index].bigblind:
             diag = 1

    diag = 0
    while diag == 0:
        if index != len(players) - 1:
            index += 1
        else:
            index = 0
        if players[index].ingame:
            diag = 1
    return index

#returns the amount of players in the game
def playersIn(returntype, players):
    if returntype:
        players_in = []
        for i in range(len(players)):
            if players[i].ingame:
                players_in.append(players[i])
    else:
        players_in = 0
        for i in range(len(players)):
            if players[i].ingame:
                players_in += 1
    return players_in

#runs the players turn
def playerTurn(players, table):
    current_raise = table.amountdown - players[0].amountdown
    # | 1 - Call/Check | 2 - Fold | 3 - Raise |
    if current_raise == 0:
        choice = intInput("| (1) - Check | (2) - Raise | ", "! need an integer 1-2 !", 0, 3)
        if choice == 2:
            choice = 3
    #if there is a raise less than an allin
    elif current_raise > 0 and current_raise < players[0].chips:
        choice = intInput("| (1) - Call %d | (2) - Fold | (3) - Raise | " % current_raise, "! need an integer 1-3 !", 0, 4)
    #if there is an allin raise
    else:
        current_raise = current_raise - (players[0].chips - current_raise)
        choice = intInput("! (1) - All-In ! | (2) - Fold | ", "! need an integer 1-2 !", 0, 3)

    if choice == 1:
        players[0].chips -= current_raise
        players[0].amountdown += current_raise
        table.pot += current_raise
    elif choice == 2:
        players[0].ingame = False
    else:
        print()
        raise_input = 0
        raise_input = intInput("How much would you like to raise? ", "! need an integer 1-%d !" % (players[0].chips - current_raise), 0, (players[0].chips + 1) - current_raise)
        current_raise += raise_input
        players[0].chips -= current_raise
        players[0].amountdown += current_raise
        table.amountdown += raise_input
        table.pot += current_raise
        print()
    return

#prints the board
def printBoard(players, table):
    print()
    for i in range(len(players)):
        if players[i].ingame:
            print("Player %d:" % (i + 1), players[i].chips, players[i].printhand)
    print()
    print("Pot =", table.pot)
    if len(table.cards) > 0:
        print(table)
    print()
    if players[0].ingame:
        print("Your Cards:", players[0].printhand)
    print()
    return

#runs a turn of the game
def turnCycle(players, table, index):
    turn_over = True
    players_in = playersIn(False, players)
    for i in range(players_in):
        print()
        print("Player", index + 1)
        printBoard(players, table)
        #overall if is for the current player
        #second if checks ingame
        if index == 0:
            if players[0].ingame and playersIn(False, players) > 1:
                playerTurn(players, table)
        else:
            if players[index].ingame and playersIn(False, players) > 1:
                computerTurn(players, table, index)
        index = turnIndex(index, players)
    turn_over = turnOver(players, table)
    while turn_over:
        print("Player", index + 1)
        printBoard(players, table)
        if index == 0:
            if players[0].ingame:
                playerTurn(players, table)
        else:
            if players[index].ingame:
                computerTurn(players, table, index)
        index = turnIndex(index, players)
        turn_over = turnOver(players, table)
    return index

#cycles the index for turnCycle
def turnIndex(index, players):
    playerNum = len(players)
    diag = 0
    while diag != 1:
        if index == playerNum - 1:
            index = 0
        else:
            index += 1
        if players[index].ingame:
            diag += 1
    return index

#checks to see if a turn is over
def turnOver(players, table):
    players_in = playersIn(True, players)

    if len(players_in) < 2:
        turn_over = False
    else:
        turn_over = 0
        for i in range(len(players_in)):
            if players_in[i].amountdown < table.amountdown:
                turn_over += 1
        if turn_over > 0:
            turn_over = True
        else:
            turn_over = False
    return turn_over

#runs a full hand
def runHand(players, blindNum):
    table = Table()
    index = handStart(players, table, blindNum)
    turnCycle(players, table, index)
    if playersIn(False, players) > 1 and not allIn(players):
        for i in range(3):
            table.addCard()
        index = nextTurn(players)
        index = turnCycle(players, table, index)
    if playersIn(False, players) > 1 and not allIn(players):
        table.addCard()
        index = nextTurn(players)
        index = turnCycle(players, table, index)
    if playersIn(False, players) > 1 and not allIn(players):
        table.addCard()
        index = nextTurn(players)
        index = turnCycle(players, table, index)
    if allIn(players):
        cards_needed = 5 - len(table.cards)
        print()
        printBoard(players, table)
        print("All in scenario")
        for i in range(cards_needed):
            input()
            table.addCard()
            printBoard(players, table)
    handOver(players, table)
    return

def main():
    playerNum = intInput("How many players? ", "! need an integer 2-8 !", 1, 9)
    chipNum = intInput("How many chips to start with? ", "! need an integer 100-1000 !", 99, 1001)
    blindNum = int(chipNum/50)

    players = []
    for i in range(playerNum):
        players.append(Player((i + 1), chipNum))

    players[1].bigblind = True
    players[0].smallblind = True

    while len(players) > 1:
        runHand(players, blindNum)

    print("Congratualations Player", players[0].number, "!")

main()
