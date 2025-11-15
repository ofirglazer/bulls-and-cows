from src.config import BullsAndCowsConfig
from src.bulls_and_cows_view import BullsAndCowsRenderer
# from src.bulls_and_cows_model import GameModel


class TestGameView:

    def test_view_initialization_human(self, capsys):
        config = BullsAndCowsConfig()
        config.human_opponent = True

        view = BullsAndCowsRenderer(config)

        # Capture printed output
        captured = capsys.readouterr()

        assert "New Game, playing against Human" in captured.out
        assert "The code length is 4" in captured.out
        assert "colors cannot be repeated in the code" in captured.out
        assert "Allowed colors are ('red', 'blue', 'cyan', 'green', 'yellow', 'orange')" in captured.out

    def test_view_initialization_bot(self, capsys):
        config = BullsAndCowsConfig()
        config.human_opponent = False

        view = BullsAndCowsRenderer(config)

        # Capture printed output
        captured = capsys.readouterr()

        assert "New Game, playing against Bot" in captured.out

    def test_view_print_guess(self, capsys):
        view = BullsAndCowsRenderer()
        capsys.readouterr()
        guess = ('a', 'b', 'c')
        number_options = 99
        view.print_guess(guess, number_options, round_number=4)

        # Capture printed output
        captured = capsys.readouterr()

        assert captured.out == f"Round 4: there are {number_options} options to the code, next guess is {guess}.\n"

    def test_view_print_guess_evaluation(self, capsys):
        view = BullsAndCowsRenderer()
        capsys.readouterr()
        feedback = (2, 3)
        view.print_guess_evaluation(feedback)

        # Capture printed output
        captured = capsys.readouterr()

        assert captured.out == f"Feedback: {feedback[0]} bulls (black pins) and {feedback[1]} cows (white pins).\n"

    def test_view_print_win(self, capsys):
        view = BullsAndCowsRenderer()
        capsys.readouterr()
        guess = ('w', 'i', 'n')
        view.print_win(guess, round_number=5)

        # Capture printed output
        captured = capsys.readouterr()

        assert captured.out == f"You win in 5 rounds! The code was {guess}.\n"

    '''def test_render_calls_draw_method(self):

        model = GameModel()
        view.render(model)

        # Should draw circles for ships
        assert mock_circle.call_count == len(model.ships) + 1  # one ship, one satellite, one star
        mock_flip.assert_called_once()'''
