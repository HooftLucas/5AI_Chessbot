from abc import ABC
import chess

"""A generic utility class"""


class Utility(ABC):

    def set_end_game(self):
        pass

    # Determine the value of the current board position (high is good for white, low is good for black, 0 is neutral)
    def board_value(self, board: chess.Board):
        pass

    def calculate_heuristic(self, board: chess.Board, debug: bool = False) -> float:
        pass

    def calculate_iterative_deepening_depth(self, board: chess.Board) -> int:
        pass