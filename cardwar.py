import random
import time

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {
    "Two": 2,   "Three": 3,  "Four": 4,
    "Five": 5,  "Six": 6,    "Seven": 7,
    "Eight": 8, "Nine": 9,   "Ten": 10,
    "Jack": 10, "Queen": 10, "King": 10,
    "Ace": 11
}


# Create object Card that contains the 2 values needed to make a card, rank and suit
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # __str__ is used to format when user print your specific card
    def __str__(self):
        return self.rank + ' of ' + self.suit

    # __repr__ is used when user print out list of cards (a deck) which will not get considered __str__
    def __repr__(self):
        return f"Card({self.suit}, {self.rank})"


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        print("Shuffling", end="", flush=True)
        time.sleep(.5)
        print(".", end="", flush=True)
        time.sleep(.5)
        print(".", end="", flush=True)
        time.sleep(.5)
        print(".", end="", flush=True)
        time.sleep(.5)
        print(".")
        random.shuffle(self.deck)
        print("Shuffle complete")

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return f"Current deck with {len(self.deck)} cards:" + deck_comp

    def give_card(self):
        return self.deck.pop()


class Player():
    def __init__(self):
        self.hand = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.hand.append(card)

    def calculate_values(self):
        for card in self.hand:
            if card.rank == "Ace":
                self.aces += 1
                self.value += values[card.rank]
                if self.value > 21:
                    self.value -= 10  # Make ace value equal 1 instead of 11
            else:
                self.value += values[card.rank]
        return self.value


class Chip():
    def __init__(self, amount):
        self.starting_amount = amount  # For leaderboard, CONSTANT
        self.amount = amount
        self.bet = 0

    def process_bet(self, win_condition):
        if win_condition == True:
            self.amount += self.bet
        else:
            self.amount -= self.bet

    def take_bet(self):
        while True:
            try:
                bet = input("How much do you want to bet? ")
            except ValueError:
                print("Must enter a number for your bet: ")
                continue
            if int(bet) <= self.amount:
                self.bet = int(bet)
                break
            else:
                print(
                    "Your bet is bigger than your chips, which is: {self.amount}")


def game_loop(still_game: bool):
    card_deck = Deck()  # New card deck created after every round
    card_deck.shuffle()

    user = Player()
    user.add_card(card_deck.give_card())
    user.add_card(card_deck.give_card())

    bot = Player()
    bot.add_card(card_deck.give_card())
    bot.add_card(card_deck.give_card())

    display_hand(user, bot)

    stand = False
    bust = False
    bot_stand = False

    # ---------------------------------------Game loop for 1 round of black jack, however many hits------
    while stand == False and bust == False:
        if bot.calculate_values < 17:
            hit(bot, card_deck)
        else:
            bot_stand = True
        choice = input("Do you want to hit or stand? ")
        if choice in ["yes", "y", "h", "hit"]:
            hit(user, card_deck)
            if user.calculate_values > 21:
                bust = True
        else:
            stand = True


def hit(player, deck):
    player.add_card(deck.give_card())


def display_hand(player, bot):
    print(f"\nBot cards: \n{bot.hand[0]}" + "\n <   ?   >" * (len(bot.hand)-1))
    print("\nYour cards: ")
    for card in player.hand:
        print(f"{card}")


def retry():
    for i in range(3):
        retry_ans = input("Do you want to play again? y/n: ")
        if retry_ans.lower() not in ["yes", "y", "no", "n"]:
            continue
        else:
            break  # Have this check to break out as soon as correct reply registered to prevent loops from stacking
    if retry_ans.lower() in ["yes", "y"]:
        return True
    else:
        return False


def record_score():
    pass


def main():
    print("\n\n")
    print("Welcome to Black Jack\nThe game will last until you run out of money or quit")
    input("Type anything to continue\n")

    # --------------------------------------Take bet----------------------
    while True:
        chip_amount = input(
            "How much money do you want to bring to the game? ")
        try:
            player_chip = Chip(int(chip_amount))
        except ValueError:
            print("Type a number")
            continue
        else:
            break

    still_game = True  # Play flag to keep playing if user answer yes.
    while still_game == True:
        still_game = game_loop(still_game)
    else:
        if retry() == False:
            record_score()
        else:
            main()


if __name__ == "__main__":
    main()
