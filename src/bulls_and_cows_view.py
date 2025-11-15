from src.config import BullsAndCowsConfig


class BullsAndCowsRenderer:

    def __init__(self, config: BullsAndCowsConfig = None):
        self.config = config or BullsAndCowsConfig()
        print(f"New Game, playing against {'Human' if self.config.human_opponent else 'Bot'}")
        print(f"The code length is {self.config.code_length},"
              f"colors {'can' if self.config.repeats_allowed else 'cannot'} be repeated in the code")
        print(f"Allowed colors are {self.config.colors}")

    @staticmethod
    def print_guess(guess: tuple[str, ...], number_options: int, round_number: int):
        print(f"Round {round_number}: there are {number_options} options to the code, next guess is {guess}.")

    @staticmethod
    def print_guess_evaluation(feedback: tuple[int, ...]):
        print(f"Feedback: {feedback[0]} bulls (black pins) and {feedback[1]} cows (white pins).")

    @staticmethod
    def print_win(guess: tuple[str, ...], round_number: int):
        print(f"You win in {round_number} rounds! The code was {guess}.")


'''
    def render(self, model):
        self.window.blit(self.bg_img, (0, 0))

        self.draw_ship(model.star)
        for ship in model.ships:
            self.draw_ship(ship)'''
