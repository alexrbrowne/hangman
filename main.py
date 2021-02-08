"""
GAME:
   - random word file
   - words are numbered
   - terminal opens, loads word list
   - player selects player 1/2, and enters name
   - terminal writes info a file for the other terminal to read
   - player one terminal picks a number
   - player ones terminal writes to file and shows player one the hangman (starts timer)
   - player twos terminal reads word number and shows player two the hangman (starts timer)
   - Both players guess at the same time
   - on winning the terminal writes the winner to file
   - both terminals shown winner


    ____
    |   |
    |   0
    |  -|-
    |  / \
    |____

    ATTEMPTS LEFT: 0


     _ _ A _ _ _ _ _ _


   GUESSES: B, C, D, E, O


    ____
    |   |
    |
    |
    |
    |____

    ____
    |   |
    |   0
    |
    |
    |____

    ____
    |   |
    |   0
    |   |
    |
    |____

    ____
    |   |
    |   0
    |  -|
    |
    |____

    ____
    |   |
    |   0
    |  -|-
    |
    |____

    ____
    |   |
    |   0
    |  -|-
    |    \
    |____

    ____
    |   |
    |   0
    |  -|-
    |  / \
    |____
"""
import sys
import random
import os
from functools import reduce
from time import sleep

LIVES = 6
men = [
    [
        "     ____",
        "     |   |",
        "     |",
        "     |",
        "     |",
        "     |____",
    ],
    [
        "     ____",
        "     |   |",
        "     |   0",
        "     |",
        "     |",
        "     |____",
    ],
    [
        "     ____",
        "     |   |",
        "     |   0",
        "     |   |",
        "     |",
        "     |____",
    ],
    [
        "     ____",
        "     |   |",
        "     |   0",
        "     |  -|",
        "     |",
        "     |____",
    ],
    [
        "     ____",
        "     |   |",
        "     |   0",
        "     |  -|-",
        "     |",
        "     |____",
    ],
    [
        "     ____",
        "     |   |",
        "     |   0",
        "     |  -|-",
        "     |  /",
        "     |____",
    ],
    [
        "     ____",
        "     |   |",
        "     |   0",
        "     |  -|-     YOU DIED",
        "     |  / \ ",
        "     |____",
    ],
]

def wipe(num):
    sys.stdout.write("\033[F\x1b[2K" * num)

class Game:

    def __init__(self, secret, player):
        self.secret = secret
        self.player = player
        self.guesses = set()
        self.attempts_left = LIVES

    def run(self):
        won = False
        letter_guess = ""
        first_run = True
        while self.attempts_left >= 0:
            if not first_run:
                wipe(14)
            self.display()
            first_run = False
            letter_guess = input("please guess a letter: ")
            if len(letter_guess.strip()) > 0:
                if letter_guess not in self.secret and letter_guess not in self.guesses:
                    self.attempts_left -= 1
                self.guesses.add(letter_guess)

                if self.did_we_win():
                    won = True
                    break
            else:
                wipe(1)
        return won

            
    def did_we_win(self):
        return reduce((lambda win, x: win and x in self.guesses), self.secret, True)
        
    def display(self):
                
        man = men[LIVES - self.attempts_left]

        guess_str = ",".join(filter(lambda l: l not in self.secret, self.guesses))
        
        print("\n".join([
            "",
            *man,
            "",
            f"ATTEMPTS LEFT: {self.attempts_left}",
            "",
            " ".join([letter if letter in self.guesses else "_" for letter in self.secret]),
            "",
            f"GUESSES: {guess_str}",
            "",
        ]))


def main():
    player = input("Which player are you? [1 or 2]")
    sys.stdout.write("\033[F")
    sys.stdout.write("\x1b[2K")
    if player == "1":
        with open("words") as f:
            lines = f.readlines()
            lineno = random.randint(0, len(lines) - 1)
            word = lines[lineno].strip()
        with open("current_game", "w") as f:
            f.write(word)
            f.flush()
        try:
            os.remove("current_winner")
        except FileNotFoundError:
            pass
    else: 
        # player 2 wait for word
        while True:
            try:
                with open("current_game") as f:
                    word = f.read().strip()
            except FileNotFoundError:
                sleep(1)
                pass               
            if len(word):
                break
    game = Game(word, player)
    won = game.run()

    if won: 
        try:
            with open("current_winner") as f:
                winner = f.read().strip()
                print(f"YOU WERE SO CLOSE BUT PLAYER {winner} WON!")
        except FileNotFoundError:    
            with open("current_winner", "w") as f:    
                f.write(player)
                f.flush()
                print("YOU ARE A GOD!")
    else:
        print(f"LOSER! WORD: {word}")     

    if player == 1:
        os.remove("current_game")

if __name__ == "__main__":
    main()
    