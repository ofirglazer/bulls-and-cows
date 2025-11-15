from src.config import BullsAndCowsConfig
from src.bulls_and_cows_controller import BullsAndCowsController


class TestGameController:

    # =============================================
    # 1. INITIALIZATION TESTING
    # =============================================

    def test_controller_initialization(self):
        """Test controller initializes with default values"""
        controller = BullsAndCowsController()

        assert hasattr(controller, 'model')
        assert hasattr(controller, 'view')
        assert hasattr(controller, 'solver')
        assert controller.running is True
        assert controller.round_number == 0

    def test_controller_initialization_different_config(self):
        """Test controller initializes with other values"""
        config = BullsAndCowsConfig()
        config.code_length = 6
        config.colors = config.colors + ('white',)
        config.human_opponent = False
        config.repeats_allowed = True

        controller = BullsAndCowsController(config)

        assert hasattr(controller, 'model')
        assert hasattr(controller, 'view')
        assert hasattr(controller, 'solver')
        assert controller.running is True


'''

    # =============================================
    # 2. EVENT HANDLING TESTING
    # =============================================

    # =============================================
    # 3. CLEANUP TESTING
    # =============================================

    def test_cleanup(self):
        """Test cleanup calls pygame.quit and prints message"""
        mock_print.assert_called_once_with("Game ended")

    # =============================================
    # 4. INTEGRATION TESTING
    # =============================================

    @patch('pygame.event.get')
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
