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
        self.ace = 0

    def add_card(self, card):
        self.hand.append(card)

    def calculate_values(self):
        current_card_val = 0
        for card in self.hand:
            if card.rank == "Ace":
                self.ace += 1
            current_card_val += values[card.rank]
            if current_card_val > 21 and self.ace > 0:
                current_card_val -= 10
                self.ace -= 1
        self.value = current_card_val
        return self.value


class Chip():
    def __init__(self, amount):
        self.starting_amount = amount  # For leaderboard percent gain, CONSTANT variable
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
                bet = input("\nHow much do you want to bet? ")
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


def retry(message="\nDo you want to restart? y/n: "):
    for i in range(3):
        retry_ans = input(message)
        if retry_ans.lower() not in ["yes", "y", "no", "n"]:
            continue
        else:
            break  # Have this check to break out as soon as correct reply registered to prevent loops from stacking
    if retry_ans.lower() in ["yes", "y"]:
        return True
    else:
        return False


def display_all(user, bot):
    print(f"\nBot: ")
    for card in bot.hand:
        print(f"{card}")
    print(f"Bot's value: {bot.calculate_values()}")
    print(f"\nUser: ")
    for card in user.hand:
        print(f"{card}")
    print(f"Your value: {user.calculate_values()}")


def record_score(player_chip: Chip):
    percent_gain_loss = round(
        player_chip.amount/player_chip.starting_amount*100-100, 2)
    print(
        F"\nYou started with {player_chip.starting_amount} and ended with {player_chip.amount}")
    record_choice = input("Do you want to record your score? y/n: ")
    if record_choice.lower() in ["no", "n"]:
        return None
    with open("leaderboard.txt", "a+") as score_file:
        name = input("What do you want your name on the leaderboard to be: ")
        if player_chip.starting_amount > player_chip.amount:
            print(
                f"Score recorded! A {abs(percent_gain_loss)}% loss")
        else:
            print(
                f"Score recorded! A {abs(percent_gain_loss)}% gain")
        score_file.write(
            f"{name} | {player_chip.starting_amount} -> {player_chip.amount} | {percent_gain_loss}%\n")


def hit_or_stand():
    while True:
        choice = input("Do you want to hit or stand: ")
        if choice.lower() in ["hit", "h", "s", "stand"]:
            return choice.lower()
        else:
            print("Wrong input, hit or stand only")


def hit(player, deck):
    player.add_card(deck.give_card())


def game_loop(still_game: bool, chip: Chip, double_down=False):
    card_deck = Deck()  # New card deck created after every match
    card_deck.shuffle()

    user = Player()
    user.add_card(card_deck.give_card())
    user.add_card(card_deck.give_card())

    bot = Player()
    bot.add_card(card_deck.give_card())
    bot.add_card(card_deck.give_card())

    chip.take_bet()
    display_hand(user, bot)

    # stand[0] = bot, stand[1] = user
    # Both have to be True to escape loop
    stand = [False, False]
    # bust[0] = bot, bust[1] = user                  |    Use list and not dict because all() and any()
    # Only one has to be True to escape loop         |    will look at keys rather than values
    bust = [False, False]

    # ---------------------------------------Game loop for 1 round of black jack-----------------------------------
    while all(stand) == False and any(bust) == False:
        if bot.calculate_values() < 17:
            hit(bot, card_deck)
            if bot.calculate_values() > 21:  # Check bust after every hit first 2 cards cannot bust
                bust[0] = True
        else:
            # If bot doesnt hit means value exceed 17, so change bot stand status to True
            stand[0] = True

        # Check incase if user already stand and bot hasnt so it doesnt keep prompting hit_or_stand
        if stand[1] == False:
            choice = hit_or_stand()
        if choice in ["h", "hit"]:
            hit(user, card_deck)
            if user.calculate_values() > 21:
                bust[1] = True
        else:
            stand[1] = True

        display_hand(user, bot)
    display_all(user, bot)
    if bust[0] == True and bust[1] != True:
        chip.process_bet(True)
        print(
            f"\nDEALER BUST! You won the round, your chips is now {chip.amount}")
    elif bust[0] != True and bust[1] == True:
        chip.process_bet(False)
        print(f"\nBUST! You lost the round, your chips is now {chip.amount}")
    elif bust[0] == True and bust[1] == True:
        print("Both dealer and player BUST, all chips returned")
    elif user.value > bot.value:
        chip.process_bet(True)
        print(
            f"\n{user.value} to {bot.value} You won the round, your chips is now {chip.amount}")
    elif user.value < bot.value:
        chip.process_bet(False)
        print(
            f"\n{user.value} to {bot.value} You lost the round, your chips is now {chip.amount}")
    else:
        print("\nDRAW! All chips returned")
    if chip.amount == 0:
        return False
    else:
        return retry("Do you want to play another round? y/n: ")


def main():
    print("\n")
    print("Welcome to Black Jack!\nThe game will last until you run out of money or quit")
    input("Type anything to continue")

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
            record_score(player_chip)
        else:
            main()


if __name__ == "__main__":
    main()
