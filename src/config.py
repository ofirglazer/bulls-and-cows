from dataclasses import dataclass
from typing import Tuple


@dataclass
class BullsAndCowsConfig:
    """Configuration for Bulls and Cows game"""

    # # Display
    # screen_width: int = 600
    # screen_height: int = 600
    # fps: int = 10

    code_length: int = 4
    colors: Tuple[str, ...] = ('red', 'blue', 'cyan', 'green', 'yellow', 'orange')
    repeats_allowed: bool = False
    human_opponent: bool = True
