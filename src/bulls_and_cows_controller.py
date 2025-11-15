from src.config import BullsAndCowsConfig
from src.bulls_and_cows_model import GameModel
from src.bulls_and_cows_view import BullsAndCowsRenderer
from src.bulls_and_cows_solver import Solver


class BullsAndCowsController:
    """Handles user input and coordinates between model and view."""

    def __init__(self, config: BullsAndCowsConfig = None):

        self.config = config or BullsAndCowsConfig()
        self.model = GameModel(self.config)
        self.view = BullsAndCowsRenderer(self.config)
        self.running = True
        self.solver = Solver(self.config, self.model)
        self.round_number = 0

    def run(self):
        """Main game loop."""

        while self.running:
            self.round_number += 1
            guess = self.solver.get_guess()
            number_options = self.solver.get_number_options()
            self.view.print_guess(guess, number_options, self.round_number)

            # get feedback on guess
            if self.config.human_opponent:
                bulls = int(input("# bulls (black pins): "))
                cows = int(input("# cows (white pins): "))
                feedback = (bulls, cows)
            else:
                feedback = self.model.evaluate_guess(self.model.code, guess)
                self.view.print_guess_evaluation(feedback)

            # process feedback
            self.solver.remove_incompatible_options(feedback)

            # exit conditions
            if int(feedback[0]) == self.config.code_length:
                self.running = False
                self.view.print_win(guess, self.round_number)

            # TODO add lose if exceeding number of rounds allowed

        # self.cleanup()

    ''''@staticmethod
    def cleanup():
        """Clean up resources."""
        # print("Game ended")'''


def main():
    controller = BullsAndCowsController()
    controller.run()


if __name__ == '__main__':
    main()
