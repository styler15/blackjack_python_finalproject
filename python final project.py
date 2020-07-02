# VARIABLES
deck = []
player_hand = []
dealer_hand = []
rounds_played = 0
player_score = 0
dealer_score = 0

# FUNCTIONS
def create_deck():
    """
    Creates and returns a deck of 52 cards. The cards are formatted with 3 digits.
    1st digit reps suit and 2nd/3rd digits rep the number

    :param: none
    :return: list of ints
    """
    
    for suits in range(1,5):
        for nums in range(1,14):
            deck.append(suits*100 + nums)
    return deck

def shuffle_deck(deck):
    """
    Shuffles the deck of cards passed into the paramater deck.

    :param deck: ordered list of cards
    :return: None
    """
    
    import random
    random.shuffle(deck)
    return

def deal_cards(deck, n):
    """
    Deals n cards from the given deck. The cards dealt
    will be removed from the deck passedand returned from
    the function in a list.

    :param deck: list of cards
    :param n: int
    :return: list of cards
    """
    
    cards = deck[:n]
    for card in cards:
        deck.remove(card)
    return cards        

def hand_value(hand):
    """
    Calculates and returns the value of the given hand.
    Always returns the BEST possible value (be careful with aces).
    
    :param hand: list of cards
    :return: int
    """
    
    final_value = 0
    ace = False
    
    for card in hand:
        numnum = card % 100
        if numnum == 1:
            final_value += 11
            ace = True
        elif numnum > 9:
            final_value += 10
        else:
            final_value += numnum
    if final_value > 21 and ace:
        final_value -= 10
    return final_value

def is_over(hand):
    """
    Returns a boolean value representing if a given
    has busted or is over 21.

    :param hand: list of cards
    :return: bool
    """
    
    value = hand_value(hand)
    if value > 21:
        return True
    else:
        return False

def compare_hands(hand1, hand2):
    """
    Comapres two hands to see if hand1 is better than hand2.
    If hand1 is better than the function returns 1, if the hands
    are the same returns 0. Otherwise if hand2 is better than 1 returns -1.

    :param hand1: int value of hand
    :param hand2: int value of hand
    :return: int
    """
    
    if hand1 > hand2:
        return 1
    elif hand2 > hand1:
        return -1
    elif hand1 == hand2:
        return 0

def get_hit_or_stay():
    """
    Gets a decision of whether to hit or stay from the user.
    Returns True if the user hits and False if the user stays. The
    function should keep asking for input until it recives "hit" or "stay".
    The case in which the user types "hit" or "stay" should not matter.

    :return: Bool
    """
    
    while True:
        response = input("Select 'hit' or 'stay': ").lower()
        if response == "hit":
            return True
        elif response == "stay":
            return False
        else:
            print("Invalid choice, did you spell 'hit' or 'stay' correctly? Try again: ")

def deal_dealercards(deck, hand):
    """
    decides whether the dealer must hit or stay based on their first two cards. If
    their total is below 17 they must hit again.

    :param deck: list of remaining cards
    :param hand: list of dealers current hand

    :return: Bool
    """

    h_value = hand_value(hand)
    while h_value <= 16:
        card = deal_cards(deck, 1)
        hand.append(card[0])
        print("Dealer must 'hit' and their new hand value is: ", hand_value(hand))
        print("Their new hand is: ", hand)
        return False
    else:
        return True
    
def score(player=0, dealer=0):
    """
    keeps cumulative score of each player if playing multiple rounds

    :param player: player wins
    :param dealer: dealer wins

    :return: int
    """
    if player > dealer:
        print("You are winning: ", player, " to ", dealer)
    elif dealer > player:
        print("You are losing: ", dealer, " to ", player)
    else:
        print("You are currently tied with the dealer.")
            


# MAINLINE (The code to play the game)

print("Welcome to the game of blackjack!")

run = True

while run:
    player_lost = False
    dealer_lost = False

    current_score = score(player_score, dealer_score)
    print(current_score)
    
    #creating and shuffling new 52 card deck
    deck.append(create_deck())
    shuffle_deck(deck)
    input("The deck has been shuffled, type 'deal' to get your 2 cards:").lower()

    #dealing first 2 player and dealer cards
    player_cards = deal_cards(deck, 2)
    player_hand = player_cards
    current_value = hand_value(player_cards)
    print("Your cards: ", player_cards, "and your hand value is: ", current_value)
    dealer_cards = deal_cards(deck, 2)
    dealer_hand = dealer_cards
    print("The dealer's cards: [", dealer_cards[0], ", hidden card]")


    #player's turn can hit or stay with 2 original cards
    choice = get_hit_or_stay()
    print()
    
    while choice:
        new_card = deal_cards(deck, 1)
        player_hand.append(new_card[0])
        print(player_hand)
        print("Your new card is: ", new_card[0])
        players_hand_value = hand_value(player_hand)
        print("Your hand value is: ", players_hand_value)

        if is_over(player_hand):
            print("You have lost this round!")
            player_lost = True
            rounds_played += 1
            dealer_score += 1
            break

        choice = get_hit_or_stay()

    if not player_lost:
        print("You have chosen to stay")
        hand1 = hand_value(player_hand)
        print("Your turn is over and your hand value is: ", hand1)

    #dealers turn to hit if hand value is less than 16
        print("It is the dealers turn and their hidden card is: ", dealer_hand[1])
        dealers_hand_value = hand_value(dealer_hand)
        while True:
            next_card = deal_dealercards(deck, dealer_hand)
            if is_over(dealer_hand):
                print("The dealer went over, YOU WIN THIS ROUND!")
                dealer_lost = True
                rounds_played += 1
                player_score += 1
                break
            elif next_card:
                print("The dealer has decided to stay, now lets compare results")
                break
    

    #deciding the winner by comparing hand values, if no one has gone over 21
    if dealer_lost == False and player_lost == False:
        hand1 = hand_value(player_hand)
        hand2 = hand_value(dealer_hand)
        print("Your hand value is:", hand1, "and the dealers hand value is:", hand2) 
        results = compare_hands(hand1, hand2)
        if results == 1:
            print("YOU WIN!")
            player_score += 1
        elif results == -1:
            print("The dealer wins!")
            dealer_score += 1
        else:
            print("It's a tie!")
        rounds_played += 1

    #Playing again? Or end game
    question = input("Do you want to play another round? (y/n): ").lower()
    if not question == "y":
        run = False
        break
