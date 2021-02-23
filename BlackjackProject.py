'''
Blackjack Milestone Project 2
Code by Andrew Lockard
Project Idea by Persian Data - Python Bootcamp on Udemy
Date: 8/9/2020

# Use Colorama to style the cards
'''

# Imports and Global Variables
from random import shuffle, randint
import time

suits = ["Hearts", "Clubs", "Spades", "Diamonds"]
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack',
            'Queen', 'King', 'Ace']
value = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9,
            'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# Classes

class Card():
    '''
    input: suit, rank
    stores: suit, rank, value, hidden

    flip_card(): toggles the hidden value
    __str__(): reports the suit and rank of the card
    '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = value[rank]
        self.hidden = False

    def __str__(self):
        return f'The {self.rank} of {self.suit}'

    def flip_card(self):
        if self.hidden == False:
            self.hidden = True
        else:
            self.hidden = False

class Deck():
    '''
    input: none
    stores: 52 generated card classes on run

    shuffle_deck(): randomly shuffles the cards within the deck
    add_new_cards(): creates a new "Deck" and adds it onto the existing deck
    deal_one(): returns a popped card off position 0
    __len__(): returns how many cards are still in the deck
    '''

    def __init__(self):
        self.cards_in_deck = []

        # Adding all cards here
        for suit in suits:
            for rank in ranks:
                self.cards_in_deck.append(Card(suit, rank))

    def shuffle_deck(self):
        shuffle(self.cards_in_deck)

    def add_new_cards(self):
        deck_2 = []
        # creates a new deck with all cards
        for suit in suits:
            for rank in ranks:
                deck_2.append(Card(suit, rank))
        # shuffles just the newly created cards
        shuffle(deck_2)
        # adds the cards into the deck
        self.cards_in_deck.extend(deck_2)


    def deal_one(self):
        '''
        Will pop off card in position zero and return it
        '''
        return self.cards_in_deck.pop(0)

    def __len__(self):
        return len(self.cards_in_deck)

class Hand():
    '''
    input: none
    stores: cards_on_table, total_value

    add_card(card): adds that card to the table and updates total value
    ace_adjust(): checks the cards on the table for an ace, adjusts its value if it needs to
    reset_hand(): resets the cards_on_table and the total_value
    __str__(): returns back the amount of cards and the total value of your hand
    '''

    def __init__(self):
        self.cards_on_table = []
        self.total_value = 0

    def add_card(self, cards):
        '''
        input: cards to be added (from deck.deal_one())
        extends/appends the card to the cards_on_table attribute, and adds the new cards value to the total value
        '''
        if type(cards) == type([]):
            self.cards_on_table.extend(cards)
            for card in cards:
                self.total_value += card.value
        else:
            self.cards_on_table.append(cards)
            self.total_value += cards.value

    def ace_adjust(self):
        '''
        Searches for an ace in the cards_on_table
        if it finds one and the current total value is larger than 21, the ace's value will be reduced to 1
        '''
        for card in self.cards_on_table:
            if card.rank == "Ace" and card.value == 11 and self.total_value > 21:
                card.value = 1
                self.total_value -= 10

    def reset_hand(self):
        self.cards_on_table = []
        self.total_value = 0

    def __str__(self):
        return f'You currently have {len(self.cards_on_table)} cards in your hand. Bringing your value up to {self.total_value}'

class Chips():
    '''
    input: none
    stores: amount in bank and amount currently in the bet - starts you out with a ramdon amount from 100-500

    win_bet(): takes the current bet amount and adds it to the bank (doubling your profit)
    lose_bet(): subtracts the current bet amount from the bank
    __str__(): returns the amount you are currently betting and the amount left in your bank after subtracting the amount you are betting
    '''

    def __init__(self):
        self.amt_bank = randint(100, 500)
        self.amt_bet = 0

    def win_bet(self):
        '''
        will add back the bet amount to the bank and set it back to 0
        '''
        self.amt_bank += self.amt_bet
        self.amt_bet = 0

    def lose_bet(self):
        '''
        Will subtract bet amount from bank and set bet back to 0
        '''
        self.amt_bank -= self.amt_bet
        self.amt_bet = 0

    def __str__(self):
        return f'You are currently betting {self.amt_bet}, and you have {self.amt_bank - self.amt_bet} left in your bank.'



# Functions
def clear_screen():
    print('\n' * 30)

def display_table(player_hand, dealer_hand, chips, deck):
    rank_to_number = {'Two':'2', 'Three':'3', 'Four':'4', 'Five':'5', 'Six':'6', 'Seven':'7', 'Eight':'8', 'Nine':'9', 'Ten':'10', 'Jack':'J',
            'Queen':'Q', 'King':'K', 'Ace':'A'}
    suit_symbol = {'Hearts':'\u2665', "Clubs":'\u2663', 'Spades':'\u2660', 'Diamonds':'\u2666'}

    # Blueprints
    top = '|---------------------------------------------------------------------------------------------------------|\n|                                                                                                         |'
    middle = '|                                                                                                         |\n|=====                                        Card Value = {0:2}                                        =====|\n|     ========                                                                               ========     |\n|             ==========                                                           ==========             |\n|                       ============              DEALER               ============                       |\n|                                   ===================================                                   |\n|                                                 PLAYER                                                  |\n|                                                                                                         |\n|                                             Card Value = {1:2}                                             |'.format(dealer_hand.total_value,player_hand.total_value)
    bottom = '|                                                                                                         |\n|                                                                                                         |\n|---------------------------------------------------------------------------------------------------------|\n|            Cards in Deck          |           Current Bet            |          Amount in Bank          |\n|                 {0:2}                |                {1:3}               |                {2:3}               |\n|---------------------------------------------------------------------------------------------------------|'.format(len(deck),chips.amt_bet,chips.amt_bank)

    # Cards 0's AND EVENS / 2 CARD NUMBER : ODDS CARD SUIT
    card_format = [0,1,
        '|                                        |-------|       |-------|                                        |\n|                                        |{0:<2}     |       |{2:<2}     |                                        |\n|                                        |       |       |       |                                        |\n|                                        |   {1}   |       |   {3}   |                                        |\n|                                        |       |       |       |                                        |\n|                                        |     {0:>2}|       |     {2:>2}|                                        |\n|                                        |-------|       |-------|                                        |',    
        '|                                |-------|       |-------|       |-------|                                |\n|                                |{0[0]:<2}     |       |{0[2]:<2}     |       |{0[4]:<2}     |                                |\n|                                |       |       |       |       |       |                                |\n|                                |   {0[1]}   |       |   {0[3]}   |       |   {0[5]}   |                                |\n|                                |       |       |       |       |       |                                |\n|                                |     {0[0]:>2}|       |     {0[2]:>2}|       |     {0[4]:>2}|                                |\n|                                |-------|       |-------|       |-------|                                |',
        '|                        |-------|       |-------|       |-------|       |-------|                        |\n|                        |{0[0]:<2}     |       |{0[2]:<2}     |       |{0[4]:<2}     |       |{0[6]:<2}     |                        |\n|                        |       |       |       |       |       |       |       |                        |\n|                        |   {0[1]}   |       |   {0[3]}   |       |   {0[5]}   |       |   {0[7]}   |                        |\n|                        |       |       |       |       |       |       |       |                        |\n|                        |     {0[0]:>2}|       |     {0[2]:>2}|       |     {0[4]:>2}|       |     {0[6]:>2}|                        |\n|                        |-------|       |-------|       |-------|       |-------|                        |',
        '|                |-------|       |-------|       |-------|       |-------|       |-------|                |\n|                |{0[0]:<2}     |       |{0[2]:<2}     |       |{0[4]:<2}     |       |{0[6]:<2}     |       |{0[8]:<2}     |                |\n|                |       |       |       |       |       |       |       |       |       |                |\n|                |   {0[1]}   |       |   {0[3]}   |       |   {0[5]}   |       |   {0[7]}   |       |   {0[9]}   |                |\n|                |       |       |       |       |       |       |       |       |       |                |\n|                |     {0[0]:>2}|       |     {0[2]:>2}|       |     {0[4]:>2}|       |     {0[6]:>2}|       |     {0[8]:>2}|                |\n|                |-------|       |-------|       |-------|       |-------|       |-------|                |',
        '|        |-------|       |-------|       |-------|       |-------|       |-------|       |-------|        |\n|        |{0[0]:<2}     |       |{0[2]:<2}     |       |{0[4]:<2}     |       |{0[6]:<2}     |       |{0[8]:<2}     |       |{0[10]:<2}     |        |\n|        |       |       |       |       |       |       |       |       |       |       |       |        |\n|        |   {0[1]}   |       |   {0[3]}   |       |   {0[5]}   |       |   {0[7]}   |       |   {0[9]}   |       |   {0[11]}   |        |\n|        |       |       |       |       |       |       |       |       |       |       |       |        |\n|        |     {0[0]:>2}|       |     {0[2]:>2}|       |     {0[4]:>2}|       |     {0[6]:>2}|       |     {0[8]:>2}|       |     {0[10]:>2}|        |\n|        |-------|       |-------|       |-------|       |-------|       |-------|       |-------|        |'
    ]
    # if theres too many cards to display on the table I created
    if len(player_hand.cards_on_table) > 6 or len(dealer_hand.cards_on_table) > 6:
        print("ERROR! You (or the dealer) has drawn too many cards to display on the table!")

        print(" ")

        print("Dealer's hand:")
        for card in dealer_hand.cards_on_table:
            print(card)
        print("Dealer's total value: " + str(dealer_hand.total_value))

        print(" ")

        print("Player's hand:")
        for card in player_hand.cards_on_table:
            print(card)
        print("Player's total value: " + str(player_hand.total_value))

        print("Chips in bank: " + str(chips.amt_bank))
        print("Current Bet: " + str(chips.amt_bet))
        print("Cards left in deck: " + len(deck))
    else:
        dealer_table = [] #[rank_to_number[dealer_hand.cards_on_table[0].rank],suit_symbol[dealer_hand.cards_on_table[0].suit],rank_to_number[dealer_hand.cards_on_table[1].rank],suit_symbol[dealer_hand.cards_on_table[1].suit]]
        player_table = [] #[rank_to_number[player_hand.cards_on_table[0].rank],suit_symbol[player_hand.cards_on_table[0].suit],rank_to_number[player_hand.cards_on_table[1].rank],suit_symbol[player_hand.cards_on_table[1].suit]]
        
        print(top)
        
        # Counts up the cards in the dealer hand and adds them to a list to print out
        if len(dealer_hand.cards_on_table) == 2: #if statement needed to stop error from occuring?
            for card in dealer_hand.cards_on_table:
                if card.hidden == True:
                    print(f"|                                        |-------|       |-------|                                        |\n|                                        |{rank_to_number[dealer_hand.cards_on_table[0].rank]:{2}}     |       |\\  \\  \\|                                        |\n|                                        |       |       |  \\  \\ |                                        |\n|                                        |   {suit_symbol[dealer_hand.cards_on_table[0].suit]}   |       | \\  \\  |                                        |\n|                                        |       |       |\\  \\  \\|                                        |\n|                                        |     {rank_to_number[dealer_hand.cards_on_table[0].rank]:{2}}|       |  \\  \\ |                                        |\n|                                        |-------|       |-------|                                        |")
                    break
            else:
                print(card_format[2].format(rank_to_number[dealer_hand.cards_on_table[0].rank],suit_symbol[dealer_hand.cards_on_table[0].suit],rank_to_number[dealer_hand.cards_on_table[1].rank],suit_symbol[dealer_hand.cards_on_table[1].suit]))
        else:
            for num in range(0,len(dealer_hand.cards_on_table)):
                dealer_table.append(rank_to_number[dealer_hand.cards_on_table[num].rank])
                dealer_table.append(suit_symbol[dealer_hand.cards_on_table[num].suit])
            print(card_format[len(dealer_hand.cards_on_table)].format(dealer_table))

        if len(dealer_hand.cards_on_table) == 2:
            for card in dealer_hand.cards_on_table:
                if card.hidden == True:
                    print(f"|                                                                                                         |\n|=====                                        Card Value = {dealer_hand.total_value - dealer_hand.cards_on_table[1].value:{2}}                                        =====|\n|     ========                                                                               ========     |\n|             ==========                                                           ==========             |\n|                       ============              DEALER               ============                       |\n|                                   ===================================                                   |\n|                                                 PLAYER                                                  |\n|                                                                                                         |\n|                                             Card Value = {player_hand.total_value:{2}}                                             |")
                    break
            else:
                print(middle)
        else:
            print(middle)
        
        # Does the same for the cards in the Player's hand
        if len(player_hand.cards_on_table) == 2:
            print(card_format[2].format(rank_to_number[player_hand.cards_on_table[0].rank],suit_symbol[player_hand.cards_on_table[0].suit],rank_to_number[player_hand.cards_on_table[1].rank],suit_symbol[player_hand.cards_on_table[1].suit]))
        else:
            for num in range(0,len(player_hand.cards_on_table)):
                player_table.append(rank_to_number[player_hand.cards_on_table[num].rank])
                player_table.append(suit_symbol[player_hand.cards_on_table[num].suit])
            print(card_format[len(player_hand.cards_on_table)].format(player_table))
       
        print(bottom)

def bet(chips):
    '''
    input: Chips class
    output: none
    Aks the player for a bet, checks if they have the amount to make that bet, and stores it in the chips class
    '''
    print("You have " + str(chips.amt_bank) + " chips in your bank")
    need_input = True
    while need_input:
        try:
            chips.amt_bet = int(input("Please Enter a Bet: "))
            if chips.amt_bet > chips.amt_bank:
                raise NameError('Over Bank Amt')
        except NameError:
            print("You don't have the funds to make that bet!")
        except:
            print("Please try again.")
        else:
            need_input = False

def cards_left_check(deck):
    if len(deck) <= 2:
        deck.add_new_cards()
        print("Out of cards, appending newly shuffled deck")
        time.sleep(1)
            
def start_round(player, dealer, deck):
    '''
    Literally just adds 2 cards to each hand and sets the second one of the daeler to hidden
    '''
    for i in range(0,2):
        cards_left_check(deck)
        player.add_card(deck.deal_one())
        dealer.add_card(deck.deal_one())
    dealer.cards_on_table[1].hidden = True

def blackjack_check(hand, chips):
    if hand.total_value == 21 and len(hand.cards_on_table) == 2:
        print("BLACKJACK!!")
        chips.amt_bet *= 1.5
        time.sleep(2)
        return False
    else:
        return True

def bust_check(hand):
    if hand.total_value > 21:
        hand.ace_adjust()
        return hand.total_value > 21
    else:
        return False

def player_turn(player, chips, deck):
    print("Your move choices are:\nDB - Double Down\nH - Hit\nS - Stand")
    need_input = True
    while need_input:
        try:
            choice = input("Please make a move:")
        except:
            print('That was an incorrect option, please type "DB", "H", or "S"')
        else:
            if choice.upper() == 'H':
                cards_left_check(deck)
                player.add_card(deck.deal_one())
                return player.total_value != 21
            elif choice.upper() == 'DB':
                if len(player_hand.cards_on_table) == 2 and chips.amt_bet *2 <= chips.amt_bank:
                    cards_left_check(deck)
                    player.add_card(deck.deal_one())
                    chips.amt_bet *= 2
                    return False
                else:
                    print("Sorry you can only Double Down when you have 2 cards in your hand or you must have the funds to double down.")
            elif choice.upper() == 'S':
                return False
            else:
                print('That was an incorrect option, please type "DB", "H", or "S"')

def dealer_turn(hand, deck, phand, pchips):
    #flip card, then begin checking for < 17 and drawing
    for card in hand.cards_on_table:
        if card.hidden == True:
            card.flip_card()
            clear_screen()
            display_table(phand, hand, pchips, deck)
            time.sleep(2)
            break
        
    hand.ace_adjust()

    while hand.total_value < 17:
        cards_left_check(deck)
        hand.add_card(deck.deal_one())
        clear_screen()
        display_table(phand, hand, pchips, deck)
        time.sleep(2)
        hand.ace_adjust()

def check_win(phand, dhand, chips):
    # if player wins
    if phand.total_value > dhand.total_value:
        chips.win_bet()
        print("You Win!!! Your bet has been added back to your bank!")
        print("Amount in Bank: " + str(chips.amt_bank))
    # if tied
    elif phand.total_value == dhand.total_value:
        chips.amt_bet == 0
        print("Tied Game! Your bet has been erased")
        print("Amount in Bank: " + str(chips.amt_bank))
    # if none of these then dealer wins
    else:
        if dhand.total_value > 21:
            chips.win_bet()
            print("Dealer busts! You win!")
            print("Amount in Bank: " + str(chips.amt_bank))
        else:  
            chips.lose_bet()
            print("Dealer wins. Your bet has been removed from your bank \nAmount in Bank: " + str(chips.amt_bank))

def play_again(phand, dhand, chips):
    # first removes cards from phand and dhand
    phand.reset_hand()
    dhand.reset_hand()
    
    #check if they have 0 chips left
    if chips.amt_bank == 0:
        print("You have 0 chips left! Thats it! No more blackjack for you! See you next time!")
        return False
    else:
        # Aks player if they would like to contine
        need_input = True
        while need_input:
            cont = input("Would you like to conintue to another hand? (Y or N): ")
            if cont.upper() == 'Y' or cont.lower() == 'yes':
                print("Starting new round...")
                clear_screen()
                return True
            elif cont.upper() == 'N' or cont.lower() == 'no':
                print("You ended with " + str(chips.amt_bank) + " chips, thanks for playing!")
                return False
            else:
                print("ERROR please try again")


if __name__ == "__main__":
    # Main Game

    # Creating all objects
    new_deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    player_chips = Chips()

    # Shuffle Deck and intro
    new_deck.shuffle_deck()
    print("Welcome to Blackjack by ItIsAndrew L!")

    # main action loop
    game_play = True
    while game_play:
        # Beginning setups, asking for bet
        bet(player_chips)
        start_round(player_hand, dealer_hand, new_deck)
        clear_screen()
        display_table(player_hand, dealer_hand, player_chips, new_deck)
        # Players turn
        player_turn_on = blackjack_check(player_hand, player_chips)
        player_bust = False
        while player_turn_on and not player_bust:
            player_turn_on = player_turn(player_hand, player_chips, new_deck)
            player_bust = bust_check(player_hand)
            clear_screen()
            display_table(player_hand, dealer_hand, player_chips, new_deck)
            if player_bust or not player_turn_on:
                time.sleep(2)
        # dealers turn
        if not player_bust:
            dealer_turn(dealer_hand, new_deck, player_hand, player_chips)
            # check for win only if not bust
            check_win(player_hand, dealer_hand, player_chips)
        else:
            player_chips.lose_bet()
            print("You bust! Your bet has been removed from your bank.")
            print("Amount in bank: " + str(player_chips.amt_bank))
        game_play = play_again(player_hand, dealer_hand, player_chips)
