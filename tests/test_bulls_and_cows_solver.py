from src.config import BullsAndCowsConfig
from src.bulls_and_cows_solver import Solver
from src.bulls_and_cows_model import GameModel


class TestSolver:

    # =============================================
    # 1. INITIALIZATION TESTING
    # =============================================

    def test_solver_initialize_possible_solution(self):
        """Test initialization with default configuration"""
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        config.code_length = 2
        config.repeats_allowed = True
        solver = Solver(config)

        # Check it's a list
        assert isinstance(solver.possible_codes, list)

        # Check all elements are tuples
        assert all(isinstance(item, tuple) for item in solver.possible_codes)

        # Check number of possible solutions
        assert len(solver.possible_codes) == len(config.colors) ** config.code_length

        # Check each tuple has elements in the length of the code
        assert all(len(item) == config.code_length for item in solver.possible_codes)

    def test_solver_initialize_possible_solution_no_repeat(self):
        """Test initialization without repeats"""
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        config.code_length = 2
        config.repeats_allowed = False
        solver = Solver(config)

        # Check number of possible solutions
        possible_number = 1
        for idx in range(config.code_length):
            possible_number = possible_number * (len(config.colors) - idx)

        assert len(solver.possible_codes) == possible_number

    def test_solver_initialize_possible_solution_different_config(self):
        """Test initialization with different configuration"""
        config = BullsAndCowsConfig()
        config.colors = ('Aa', 'Bb', 'Cc', 'Dd', 'Ee', 'Ff', 'Gg', 'Hh')
        config.code_length = 4
        config.repeats_allowed = True
        solver = Solver(config)

        # Check it's a list
        assert isinstance(solver.possible_codes, list)

        # Check all elements are tuples
        assert all(isinstance(item, tuple) for item in solver.possible_codes)

        # Check number of possible solutions
        assert len(solver.possible_codes) == len(config.colors) ** config.code_length

        # Check each tuple has elements in the length of the code
        assert all(len(item) == config.code_length for item in solver.possible_codes)

    def test_get_guess(self):
        """Test getting a valid guess"""
        solver = Solver()
        guess = solver.get_guess()

        # Check it's a tuple
        assert isinstance(guess, tuple)

        # Check length of guess is the length of the code
        assert len(guess) == solver.config.code_length

    def test_get_number_options_with_repeats(self):
        """Test getting valid number of remaining options"""
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        config.code_length = 5
        config.repeats_allowed = True
        solver = Solver(config)
        number_options = solver.get_number_options()

        # Check receiving int
        assert isinstance(number_options, int)
        # Check correct number of possible solutions
        assert number_options == len(config.colors) ** config.code_length

    def test_get_number_options_no_repeats(self):
        """Test getting valid number of remaining options"""
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')
        config.code_length = 4
        config.repeats_allowed = False
        solver = Solver(config)
        number_options = solver.get_number_options()

        # Check receiving int
        assert isinstance(number_options, int)
        # Check correct number of possible solutions
        possible_number = 1
        for idx in range(config.code_length):
            possible_number = possible_number * (len(config.colors) - idx)
        assert number_options == possible_number

    def test_validate_feedback_correct(self):
        config = BullsAndCowsConfig()
        model = GameModel(config)
        solver = Solver(config=config, model=model)

        bulls = 2
        cows = 1
        feedback = (bulls, cows)
        assert solver.validate_feedback(feedback) is True

    def test_validate_feedback_not_number(self):
        config = BullsAndCowsConfig()
        model = GameModel(config)
        solver = Solver(config=config, model=model)

        bulls = '2'
        cows = 3
        feedback = (bulls, cows)
        assert solver.validate_feedback(feedback) is False

    def test_validate_feedback_negative(self):
        config = BullsAndCowsConfig()
        model = GameModel(config)
        solver = Solver(config=config, model=model)

        bulls = 1
        cows = -3
        feedback = (bulls, cows)
        assert solver.validate_feedback(feedback) is False

        bulls = -2
        cows = 1
        feedback = (bulls, cows)
        assert solver.validate_feedback(feedback) is False

    def test_validate_feedback_max(self):
        config = BullsAndCowsConfig()
        config.code_length = 5
        model = GameModel(config)
        solver = Solver(config=config, model=model)

        bulls = 1
        cows = 6
        feedback = (bulls, cows)
        assert solver.validate_feedback(feedback) is False

        bulls = 7
        cows = 0
        feedback = (bulls, cows)
        assert solver.validate_feedback(feedback) is False

    def test_validate_feedback_max_total(self):
        config = BullsAndCowsConfig()
        config.code_length = 5
        model = GameModel(config)
        solver = Solver(config=config, model=model)

        bulls = 1
        cows = 5
        feedback = (bulls, cows)
        assert solver.validate_feedback(feedback) is False

        bulls = 3
        cows = 3
        feedback = (bulls, cows)
        assert solver.validate_feedback(feedback) is False

    def test_remove_incompatible_options(self):
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd')
        config.code_length = 2
        config.repeats_allowed = True
        model = GameModel(config)
        solver = Solver(config=config, model=model)

        model.code = ('a', 'b')
        guess = ('a', 'a')
        solver.last_guess = guess  # done manually for this test instead of get_guess to determine a specific guess
        feedback = model.evaluate_guess(model.code, guess)
        solver.remove_incompatible_options(feedback)
        assert solver.possible_codes == [('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'a'), ('c', 'a'), ('d', 'a')]


'''
    # =============================================
    # 2. EVENT HANDLING TESTING
    # =============================================

    # =============================================
    # 3. CLEANUP TESTING
    # =============================================

    # =============================================
    # 4. INTEGRATION TESTING
    # =============================================
'''
