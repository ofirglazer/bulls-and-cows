from src.bulls_and_cows_model import GameModel
from src.config import BullsAndCowsConfig
from itertools import permutations, product
from random import choice, seed
# guesses = ListPerm(code_length, colors, is_color_reuse_allowed)


class Solver:

    def __init__(self, config: BullsAndCowsConfig = None, model: GameModel = None):
        seed()
        self.last_guess = None
        self.model = model

        self.config = config or BullsAndCowsConfig()

        # initialize list of all possible guesses
        if self.config.repeats_allowed:
            possible_codes_itertools = product(self.config.colors, repeat=self.config.code_length)
        else:
            possible_codes_itertools = permutations(self.config.colors, self.config.code_length)
        self.possible_codes = list(possible_codes_itertools)

    def get_guess(self) -> tuple[str, ...]:
        if self.get_number_options() == 0:
            raise "Incompatible results"
        self.last_guess = choice(self.possible_codes)
        return self.last_guess

    def get_number_options(self) -> int:
        return len(self.possible_codes)

    def remove_incompatible_options(self, feedback: tuple[int, ...]):
        # remove options incompatible with latest guess-feedback couple
        remaining_options = list()
        for option in self.possible_codes:
            option_evaluate = self.model.evaluate_guess(option, self.last_guess)
            if option_evaluate == feedback:
                remaining_options.append(option)  # option compatible with guess feedback
        self.possible_codes = remaining_options


'''
        #Find number of remaining guesses for every result of every guess
        max_remaining = list()
        for guess in self.listPerm:  # for every possible guess
            remaining = list()
            for result in results:  # check for every possible result
                self.matching(guess, result)  # how many valid guess would remain
                remain = sum(1 for perm in self.matches if perm is True)
                # print("guess",guess,"result",result,"remaining",remain)
                remaining.append(remain)  # score for each guess
            max_remaining.append(max(remaining))

        # find guess with minimum remaining, not zero
        idx = max_remaining.index(min([i for i in max_remaining if i > 0]))
        return self.listPerm[idx]'''
