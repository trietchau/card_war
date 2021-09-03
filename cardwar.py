import random
import time

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {
    "Two": 2,   "Three": 3,  "Four": 4,
    "Five": 5,  "Six": 6,    "Seven": 7,
    "Eight": 8, "Nine": 9,   "Ten": 10,
    "Jack": 11, "Queen": 12, "King": 13,
    "Ace": 14
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
        self.deck = deck = []
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
        self.deck = random.shuffle(self.deck)
        print("Shuffle complete")

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return f"Current deck with {len(self.deck)} cards:" + deck_comp

    def give_card(self):
        return self.deck.pop()


class Player():
    def __init__(self, bal):
        self.bal = bal

    def bet(self, amount):
        pass

    def double_down(self, prev_bet):
        if prev_bet * 2 <= self.bal:
            pass

    def add_sub_bet(self, bet, win_condition):
        if win_condition == True:
            self.bal += bet


new_deck = Deck()
print(new_deck)


def game_loop():
    print("\n\n\n")
    print("Game will last until you run out of money or ")
    card_deck = Deck()  # New card deck created after every round
    card_deck.shuffle()


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


def main():
    still_game = True  # Play flag to keep playing if user answer yes.
    while still_game == True:
        game_loop()
        still_game = retry()
    else:
        record_score()


if __name__ == "__main__":
    main()
