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
                # Create full deck when object instantiated
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

    def add_card(self, card):
        self.hand.append(card)

    def calculate_values(self):
        current_card_val = 0
        for card in self.hand:
            if card.rank == "Ace":
                current_card_val += values[card.rank]
                # When add ace there's a chance it will bust, if that's the case then make the previous ace = 1
                if current_card_val > 21:
                    current_card_val -= 10
            else:
                current_card_val += values[card.rank]
        self.value = current_card_val
        return self.value


class Chip():
    def __init__(self, amount):
        self.starting_amount = amount  # For leaderboard percent gain, CONSTANT variable
        self.amount = amount
        self.bet = 0

    def process_bet(self, win_condition, draw=False):
        if win_condition == True and draw == False:
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
                    f"Your bet is bigger than your chips, which is: {self.amount}")


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


def hit_or_stand():
    pass


def hit(player, deck):
    player.add_card(deck.give_card())


def game_loop(still_game: bool, chip):
    card_deck = Deck()  # New card deck created after every round
    card_deck.shuffle()

    user = Player()
    user.add_card(card_deck.give_card())
    user.add_card(card_deck.give_card())

    bot = Player()
    bot.add_card(card_deck.give_card())
    bot.add_card(card_deck.give_card())

    chip.take_bet()

    display_hand(user, bot)

    # Both have to be True to escape loop
    stand = [False, False]  # stand[0] = bot, stand[1] = user
    # Only one has to be True to escape loop
    bust = [False, False]   # bust[0] = bot, bust[1] = user

    # ---------------------------------------Game loop for 1 round of black jack, however many hits------
    while all(stand) == False and any(bust) == False:
        if bot.calculate_values() < 17:
            hit(bot, card_deck)
            print(f"Bot: {bot.calculate_values()}")
            if bot.calculate_values() > 21:
                bust[0] = True
        else:
            stand[1] = True

        choice = input("\nDo you want to hit or stand? ")
        if choice in ["h", "hit"]:
            hit(user, card_deck)
            display_hand(user, bot)
            if user.calculate_values() > 21:
                bust[1] = True
        else:
            bust[1] = True


def main():
    print("\n")
    print("Welcome to Black Jack!\nThe game will last until you run out of money or quit")
    input("Type anything to continue\n")

    # ------------------------------Set starting amount of money----------------------------------
    while True:
        chip_amount = input(
            "How much money do you want to bring to the game? ")
        try:
            player_chip = Chip(int(chip_amount))
        except ValueError:
            print("Type a number")
        else:
            break

    still_game = True  # Play flag to keep playing if user answer yes.
    while still_game == True:
        still_game = game_loop(still_game, player_chip)
    else:
        if retry() == False:
            record_score()
        else:
            main()


if __name__ == "__main__":
    main()
