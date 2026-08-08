import random
import string


class word_generator:
    def __init__(
        self,
    ):
        self.words = [
            "python",
            "variable",
            "function",
            "iterator",
            "notebook",
            "pipeline",
            "dataset",
            "computer",
            "research",
            "analytics",
            "boom"
        ]

    def get_random_word(self):
        return random.choice(self.words)


class word_guessing_game:
    def __init__(self, word_generator, max_lives):
        self.max_lives = max_lives
        self.word_generator = word_generator

    def make_blanks(self, word):
        return ["_" for _ in word]

    def prompt_for_letter(self, used_letters):
        while True:
            guess = input("Guess a letter: ").strip().lower()
            if len(guess) != 1 or guess not in string.ascii_lowercase:
                print(" → Please enter a single A-Z letter.")
                continue
            if guess in used_letters:
                print(" → You already tried that letter.")
                continue
            return guess

    def reveal_letters(self, word, blanks, letter):
        for i, ch in enumerate(word):
            if ch == letter and blanks[i] == "_":
                blanks[i] = letter
                return True
        return False

    def handle_turn(self, used_letters, secret_word, blanks):
        # Ask the user to guess a letter
        guess = self.prompt_for_letter(used_letters)
        used_letters.add(guess)
        # Is the guessed letter in the word?
        if self.reveal_letters(secret_word, blanks, guess):
            print("\n Well done, Nice job! You found a letter.")
            print(" ".join(blanks))
            # Are all blanks filled?
            if self.all_blanks_filled(blanks):
                print("\n Congratulation! You guessed the word!")
                print(f"Word: {secret_word}")
                print("YOU WIN")
                return True
        else:
            # Lose a life
            self.max_lives -= 1
            print(f"\nNope. You lose a life. Lives left: {self.max_lives}")
            print(" ".join(blanks))
            # Have they run out of lives?
            if self.max_lives <= 0:
                print("\n Out of lives & Sad story!")
                print(f"The word was: {secret_word}")
                print("YOU LOST")
                return True

    def play_game(self):
        secret_word = self.word_generator.get_random_word()
        blanks = self.make_blanks(secret_word)
        used_letters = set()
        print("\nWelcome to Word Guessing!")
        print(f"The word has {len(secret_word)} letters.")
        print(" ".join(blanks))
        while True:
            if self.handle_turn(used_letters, secret_word, blanks):
                break

    def all_blanks_filled(self, blanks):
        return "_" not in blanks

def play_game(max_lives=6):
    generator = word_generator()
    guess_the_word_game = word_guessing_game(generator, max_lives)
    guess_the_word_game.play_game()

if __name__ == "__main__":
    play_game()
