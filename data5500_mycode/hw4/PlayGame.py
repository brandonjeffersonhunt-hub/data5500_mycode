from DeckOfCards import * #bring over the code provided by Andy. Move the classes to this file so I can make objects with them

class Player:   #Create a new class called player
    def __init__(self, name: str, is_dealer: bool = False):
        self.name = name
        self.is_dealer = is_dealer
        self.hand = []      #create an empty list to represent the players hand. will contain the cards once dealt

    def add_card(self, card: Card):    #create method to deal the cards to the players hand.
        self.hand.append(card)      #Card is inputed to the self.hand list

    def reset_hand(self):       #Create function to empty the hand so you can play a round again and lose all your money quickly
        self.hand.clear()       #Chat taught me about the .clear function, have not used that before so I asked what to use

    def value(self):            #function to check what the value of the hand is
        total = 0           #running total of the value
        aces = 0            #keep track of how many aces there are
    
        for c in self.hand:
            total += c.val          #add all the cards together to get the value of the hand
            if c.face  == "Ace":
                aces += 1           #if the face value of the card is an ace then we add that to the running total of aces in the players hand

        while total > 21 and aces > 0:          #if the players hand value is greater than 21 and they have 1 or more ace then we adjust the score
            total -= 10                     #makes the value of that ace 1 instead of 11
            aces -= 1                       #removes an ace from the running total

        return total                #lets see where we are at with the hand value

    def is_busted(self):            #check to see if you went over 21
        return self.value() > 21    #returns this function if the value >21

    def hand_string(self, hide_first: bool = False):        #function to hide the first card of the dealer's hand
        parts = []                                          #hold the string version of the cards
        for i, c in enumerate(self.hand):              #enumerate gives us the index # for each card and the actual card 
            if hide_first and self.is_dealer and i == 0:       #if the player is the dealer, and it is the first card of the hand
                parts.append("[Hidden]")                            #then you append the list with the hand to hidden
            else:
                parts.append(f"{c.face} of {c.suit}")         #if not then you just list the cards. Used if player is not dealer
        
        shown_value = "??" if (hide_first and self.is_dealer) else str(self.value())   #dont display value if dealer, if player show calue
        return f"{self.name}: {', '.join(parts)} (value: {shown_value})"

def play_round():                                   #function to play the game
    print("Alright, let's play some Blackjack\n")     #friendly welcome before I take your money

    deck = DeckOfCards()                            #grab the deck
    print("Deck before being shuffled:")            #print the deck before it gets shuffled to prove tha tthe shuffle worked
    deck.print_deck()

    deck.shuffle_deck()                             #shuffle the cards
    print("Deck after shuffle:")                     #Shuffled cards printed
    deck.print_deck()
    print()                                     #blank line for readability

    user = Player("You")                            #assign the roles. You are the player
    dealer = Player("Dealer", is_dealer = True)     #dealer=True so you dont show their hand

    for _ in range(2):                      #initial deal of 2 cards
        user.add_card(deck.get_card())      #give a card to player
        dealer.add_card(deck.get_card())    #give card to dealer
    print(user.hand_string())                   #print users hand
    print(dealer.hand_string(hide_first = True))               #print dealers hand hiding the first one

    while True:                                  #loop to keep game going until bust or stand
        
        print(user.hand_string())                   #print users hand

        choice = input("Would you like to hit (y/n):").strip().lower()   #ask user to hit or not. strip and lowcase their message
        if choice == "y":                           #if the user types y
            user.add_card(deck.get_card())         #add a card to the user hand
            last_card = user.hand[-1]                #i learned from chat that the way to get the last item in a list is this way
            print(f"You drew: {last_card.face} of {last_card.suit}")        #tell them what they drew
            print(f"Your total is now {user.value()}")                  #tell user new total
            if user.is_busted():                                    #if new total > 21
                print("You busted, dealer wins:(")                              
                return                                                  #round ends
        elif choice =="n":                                       #if user wants to stand
            print("You choose to stand")
            break
        else:
            print("invalid entry, please type 'y' or 'n'.")     #control for misinputs
            continue
    
    print("The dealer reveals his hand:")       #if they chose to stand have the dealer reveal his cards
    print(dealer.hand_string(hide_first = False))   #now we can un-hide the dealers first card

    while dealer.value() < 17:                     #ruberic said to have dealer hit until they have a card total >17
        dealer.add_card(deck.get_card())            #add card to dealer hand
        last = dealer.hand[-1]                      #select las card added
        print(f"The dealer hits and draws {last.face} of {last.suit}")      #display what the dealer drew
        print(f"The dealer's total is now {dealer.value()}")            #display the dealers total
        if dealer.is_busted():                          #if the dealer busts
            print("The dealer busted. You win! :)")     #notify the user
            return

    print(f"The dealer stands with {dealer.value()}\n")     #if the dealer is already at or gets to a value > 17

    user_total = user.value()       #new varables for easier coding
    dealer_total = dealer.value()   

    if dealer_total >= user_total:              #if the dealer beats you
        print(f"Your score is {user_total}, but the dealer's is {dealer_total}. You lose :()")
    else:                                           #if the dealer busts
        print(f"Dealer score is {dealer_total}, but your score is {user_total}. You win! :)")
    
    print("\n(End of round.)")

def main():                                 #a little loop to replay the game for the degenerates
    while True: 
        play_round()                        # play one round

        again = input("\nWould you like to play again? (y/n): ").strip().lower()        #ask to play again
        if again != "y":
            print("Thanks for playing! Goodbye :)")
            break

if __name__ == "__main__":
    main()
    




