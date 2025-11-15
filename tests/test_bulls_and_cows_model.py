from src.config import BullsAndCowsConfig
from src.bulls_and_cows_model import randomize_code, GameModel


class TestGame:

    # =============================================
    # 1. INITIALIZATION TESTING
    # =============================================

    def test_randomize_code_no_repeats(self):
        """Test randomize code without repeats"""
        code_length = 4
        colors = ('a', 'b', 'c', 'd', 'e', 'f')
        repeats_allowed = False
        code = randomize_code(code_length=code_length, colors=colors, repeats_allowed=repeats_allowed)
        assert isinstance(code, tuple)
        assert len(code) == code_length
        # number of unique values is the code length because no repeats allowed
        assert len(list(set(code))) == code_length

    def test_randomize_code_with_repeats(self):
        """Test randomize code without repeats"""
        code_length = 8
        colors = ('a', 'b', 'c', 'd', 'e', 'f')
        repeats_allowed = True
        code = randomize_code(code_length=code_length, colors=colors, repeats_allowed=repeats_allowed)
        assert isinstance(code, tuple)
        assert len(code) == code_length
        # number of unique values is the code length because no repeats allowed
        assert len(list(set(code))) < code_length

    def test_game_initialization(self):
        """Test model initializes"""
        game = GameModel()

        assert hasattr(game, 'code')

    def test_game_initialization_different_config(self):
        """Test model initializes with other values"""
        config = BullsAndCowsConfig()
        config.code_length = 6
        config.colors = config.colors + ('white',)
        config.human_opponent = False
        config.repeats_allowed = True
        game = GameModel()

        assert hasattr(game, 'code')

    def test_evaluate_guess_no_repeats_correct(self):
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        config.code_length = 3
        game = GameModel(config)

        code = ('a', 'b', 'c')

        # guess correct
        guess = ('a', 'b', 'c')
        feedback = game.evaluate_guess(code, guess)
        bulls = feedback[0]
        cows = feedback[1]
        assert isinstance(feedback, tuple)
        assert bulls == 3
        assert cows == 0

    def test_evaluate_guess_no_repeats_none(self):
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        config.code_length = 3
        game = GameModel(config)

        code = ('a', 'b', 'c')

        # guess none
        guess = ('d', 'e', 'f')
        feedback = game.evaluate_guess(code, guess)
        bulls = feedback[0]
        cows = feedback[1]
        assert bulls == 0
        assert cows == 0

    def test_evaluate_guess_no_repeats_mixed(self):
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        config.code_length = 3
        game = GameModel(config)

        code = ('a', 'b', 'c')

        # guess bulls, cows, none
        guess = ('a', 'c', 'd')
        feedback = game.evaluate_guess(code, guess)
        bulls = feedback[0]
        cows = feedback[1]
        assert bulls == 1
        assert cows == 1

    def test_evaluate_guess_with_repeats_correct(self):
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        config.code_length = 3
        game = GameModel(config)

        code = ('a', 'b', 'b')

        # guess correct
        guess = ('a', 'b', 'b')
        feedback = game.evaluate_guess(code, guess)
        bulls = feedback[0]
        cows = feedback[1]
        assert isinstance(feedback, tuple)
        assert bulls == 3
        assert cows == 0

    def test_evaluate_guess_with_repeats_none(self):
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        config.code_length = 3
        game = GameModel(config)

        code = ('a', 'b', 'b')

        # guess none
        guess = ('d', 'e', 'f')
        feedback = game.evaluate_guess(code, guess)
        bulls = feedback[0]
        cows = feedback[1]
        assert bulls == 0
        assert cows == 0

    def test_evaluate_guess_with_repeats_1bull(self):
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        config.code_length = 3
        game = GameModel(config)

        code = ('a', 'b', 'b')

        # guess bulls, cows, none
        guess = ('d', 'b', 'e')
        feedback = game.evaluate_guess(code, guess)
        bulls = feedback[0]
        cows = feedback[1]
        assert bulls == 1
        assert cows == 0

    def test_evaluate_guess_with_repeats_1cow(self):
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        config.code_length = 3
        game = GameModel(config)

        code = ('a', 'b', 'b')

        # guess bulls, cows, none
        guess = ('b', 'd', 'e')
        feedback = game.evaluate_guess(code, guess)
        bulls = feedback[0]
        cows = feedback[1]
        assert bulls == 0
        assert cows == 1

    def test_evaluate_guess_with_repeats_1bull1cow(self):
        config = BullsAndCowsConfig()
        config.colors = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        config.code_length = 3
        game = GameModel(config)

        code = ('a', 'b', 'b')

        # guess bulls, cows, none
        guess = ('b', 'b', 'd')
        feedback = game.evaluate_guess(code, guess)
        bulls = feedback[0]
        cows = feedback[1]
        assert bulls == 1
        assert cows == 1


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

    def test_model_view_coordination(self, mock_get_events, controller_with_mocks):
        """Test that controller properly coordinates model and view"""
        mock_get_events.return_value = []

        # Simulate game loop actions
        controller_with_mocks.mock_model.update()
        controller_with_mocks.mock_view.render(controller_with_mocks.mock_model)

        # Verify coordination
        controller_with_mocks.mock_model.update.assert_called()
        controller_with_mocks.mock_view.render.assert_called_with(controller_with_mocks.mock_model)
        '''
