#!/usr/bin/python

import random

#list_of_suits = ["H","D","S","C"]
list_of_suits = [u'\u2665',u'\u2666',u'\u2660',u'\u2663']
list_of_cards = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
dict_of_payouts = {
    'None': 0,
    'One Pair': 1,
    'Two Pairs': 2,
    'Three Of A Kind': 3,
    'Straight': 4,
    'Flush': 6,
    'Full House': 9,
    'Four Of A Kind': 25,
    'Straight Flush': 50,
    'Royal Flush': 800
}

class CardDeck:

    def __init__(self):
        self.card_list = []

    def initialize_deck(self):
        self.card_list = []
        for suit in list_of_suits:
            for card in range(0,len(list_of_cards)):
                self.card_list.append([card, suit])

    def deal_card(self,num):
	cards_to_deal = []
	for cards in range(0,num):
            number_to_deal = random.randint(0,(len(self.card_list)-1))
            cards_to_deal.append(self.card_list.pop(number_to_deal))
        return cards_to_deal

class Player:

    def __init__(self,name,money=100):
        self.hand = []
        self.name = name
        self.money = money

    def initialize_hand():
        self.hand = []

def check_hand(player_hand):

    hand_type = 'None'

    # Create Hand Histogram
    hand_histogram = [int(0)] * 13
    for cards in player_hand:
        hand_histogram[int(cards[0])] += 1

    # Check for pairings
    if hand_histogram.count(2) == 1 and hand_histogram.count(3) == 0:
        if hand_histogram.index(2) >= 9:
            hand_type = 'One Pair'
    elif hand_histogram.count(2) == 2:
        hand_type = 'Two Pairs'
    elif hand_histogram.count(3) == 1 and hand_histogram.count(2) == 0:
        hand_type = 'Three Of A Kind'
    elif hand_histogram.count(3) == 1 and hand_histogram.count(2) == 1:
        hand_type = 'Full House'
    elif hand_histogram.count(4) == 1:
        hand_type = 'Four Of A Kind'

    straight = False
    flush = False
    straight_flush = False

    # Check For Straight
    for straight_start in range(0,10):
        if hand_histogram[straight_start:straight_start+5] == [1,1,1,1,1]:
            straight = True
            hand_type = 'Straight'
    if hand_histogram[0:4] == [1,1,1,1] and hand_histogram[12] == 1:
        straight = True
        hand_type = 'Straight'

    # Check For Flush
    for suit in list_of_suits:
        suit_count = 0
        for card in player_hand:
            if card[1] == suit:
                suit_count += 1
        if suit_count == 5:
            flush = True
            hand_type = 'Flush'

    # Check For Straight Flush
    if straight and flush:
        straight_flush = True
        hand_type = 'Straight Flush'

    # Check For Royal Flush
    if straight_flush and sorted(player_hand)[0][0] == 8:
        hand_type = 'Royal Flush'

    wager_multiplier = dict_of_payouts[hand_type]
    return (hand_type,wager_multiplier)

def print_payouts():
    print "*** Payouts - Times Initial Bet ***"
    payouts_list = sorted(dict_of_payouts.values())[::-1]
    for payout in payouts_list:
        for hand, payouts in dict_of_payouts.items():
            if payout == payouts:
                print hand, ":", str(payout)
    print

def print_hand(hand_to_print):
    print
    print "1   2   3   4   5"
    print "--  --  --  --  --"
    for card in hand_to_print:
        print "%s%s " % (list_of_cards[card[0]],card[1]),
    print

def print_hand_w_hold(hand_to_print,hold_list_loc):
    print
    for card_number in range(1,6):
        if card_number in hold_list_loc:
            print str(card_number) + "H ",
        else:
            print str(card_number) + "  ",
    print "\n--  --  --  --  --"
    for card in hand_to_print:
        print "%s%s " % (list_of_cards[card[0]],card[1]),
    print

def Main() :
    keep_playing = True

    while keep_playing:
        
        # Print Current Bankroll And Ask For Wager
        print "Current bankroll: ", player.money
        print
        player_wager = raw_input("How much would you like to wager? ")

        # Check Wager Is Appropriate Value
        while player_wager.isdigit() == False or int(player_wager) > player.money or int(player_wager) == 0:
            print "Invalid input.  Must be a number between 1 and %s" % player.money
            player_wager = raw_input("How much would you like to wager? ")

        # Initialize The Deck
        deck.initialize_deck()

        # Deal The Player Hand
        player.hand = deck.deal_card(5)

        # Print Player Hand
        print_hand(player.hand)

        # Get Hold List From Player
        hold_number = 0
        hold_list = []
        complete_discard = False
        while complete_discard == False:
            print
            hold_number = raw_input("Enter a card number to hold/unhold or 'd' to complete discards: ")
            if hold_number.isdigit() == True and int(hold_number) >= 1 and int(hold_number) <= 5 and int(hold_number) not in hold_list:
                hold_list.append(int(hold_number))
                print_hand_w_hold(player.hand,hold_list)
            elif hold_number.isdigit() == True and int(hold_number) >= 1 and int(hold_number) <= 5 and int(hold_number) in hold_list:
                hold_list.remove(int(hold_number))
                print_hand_w_hold(player.hand,hold_list)
            elif hold_number == "d":
                complete_discard = True
            else:
                print "Invalid input.  Please enter a card number 1-5 or 'd' to complete discard",

        # Complete Discards
        for discard in range(1,6):
            if discard not in hold_list:
                player.hand[discard-1] = deck.deal_card(1)[0]

        # Print Final Player Hand
        print_hand(player.hand)

        # Check Hand For Matches, Get Payout
        hand_type,wager_multiplier = check_hand(player.hand)
        player_winnings = int(player_wager) * wager_multiplier

        # Pay The Player
        player.money = player.money - int(player_wager) + player_winnings

        # Announce Winnings
        if wager_multiplier == 0:
            print "\nNothing - You lost your wager of %s\n" % player_wager
        else:
            print "\n%s - You won %s on your hand!\n" % (hand_type,player_winnings)
       
        # Game Over, You Ran Out Of Money
        if player.money == 0:
            print "Game Over - You Ran Out Of Money!"
            keep_playing = False


### Begin The Game

# New object for deck of cards
deck = CardDeck()

# New object for player and initial bankroll
player = Player('Player1',200)

# Print a listing of payouts
print_payouts()

# Start Playing
Main()
