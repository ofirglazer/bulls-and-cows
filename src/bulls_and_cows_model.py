from random import choices, sample, seed
from src.config import BullsAndCowsConfig


def randomize_code(code_length: int = 4, colors: tuple[str, ...] = ('red', 'blue', 'cyan', 'green', 'yellow', 'orange'),
                   repeats_allowed: bool = False) -> tuple[str, ...]:
    seed()
    if repeats_allowed:
        return tuple(choices(colors, k=code_length))
    else:
        return tuple(sample(colors, k=code_length))


class GameModel:

    def __init__(self, config: BullsAndCowsConfig = None):
        self.config = config or BullsAndCowsConfig()
        self.num_colors = len(self.config.colors)

        self.code = randomize_code(self.config.code_length, self.config.colors, self.config.repeats_allowed)

    def evaluate_guess(self, code: tuple[str, ...], guess: tuple[str, ...]) -> tuple[int, int]:
        bulls_and_cows = 0
        bulls = 0

        # total appearances of all guessed colors in the code
        for color in self.config.colors:
            bulls_and_cows = bulls_and_cows + min(guess.count(color), code.count(color))

        # locate bulls
        for idx in range(self.config.code_length):
            if guess[idx] == code[idx]:
                bulls = bulls + 1
        cows = bulls_and_cows - bulls
        return (bulls, cows)


'''def main():
    seed(0)
    game = GameModel()
    pass


if __name__ == '__main__':
    main()'''
