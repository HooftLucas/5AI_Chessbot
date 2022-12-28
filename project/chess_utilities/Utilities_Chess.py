import chess
from project.chess_utilities.utility import Utility

pawn_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]
knights_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishops_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rooks_table = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queens_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kings_table_middlegame = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]
kings_table_endgame = [
    -50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50]
pawn_value = 100
knight_value = 320
bishop_value = 330
rook_value = 500
queen_value = 900
king_value = 200000


class ChessUtility(Utility):
    def __init__(self, weightVector: list[float]) -> None:
        self.weightVector: list[float] = weightVector
        self.endGame = False

    def set_end_game(self):
        self.endGame = True

    def calculate_heuristic(self, board: chess.Board) -> float:
        """
        Main function which returns the value of a board state
        :param board:
        :return:
        """
        features = [
            self.feature_killer_move(board),
            self.feature_material_value(board),
            self.feature_piecesquare_value(board),
            self.feature_mobility_value(board)
        ]
        boardValue: float = 0.0
        for feature, weight in zip(features, self.weightVector):
            boardValue += feature * weight
        return boardValue

    def feature_killer_move(self, board: chess.Board):
        if board.is_checkmate():
            if board.turn:
                return -9999
            return 9999
        return 0

    def feature_material_value(self, board: chess.Board):
        material_value = 0
        material_value += len(board.pieces(chess.PAWN, board.turn)) * pawn_value
        material_value += len(board.pieces(chess.BISHOP, board.turn)) * bishop_value
        material_value += len(board.pieces(chess.KNIGHT, board.turn)) * knight_value
        material_value += len(board.pieces(chess.ROOK, board.turn)) * rook_value
        material_value += len(board.pieces(chess.QUEEN, board.turn)) * queen_value
        material_value += len(board.pieces(chess.KING, board.turn)) * king_value

        material_value_enemy = 0
        material_value_enemy += len(board.pieces(chess.PAWN, not board.turn)) * pawn_value
        material_value_enemy += len(board.pieces(chess.BISHOP, not board.turn)) * bishop_value
        material_value_enemy += len(board.pieces(chess.KNIGHT, not board.turn)) * knight_value
        material_value_enemy += len(board.pieces(chess.ROOK, not board.turn)) * rook_value
        material_value_enemy += len(board.pieces(chess.QUEEN, not board.turn)) * queen_value
        material_value_enemy += len(board.pieces(chess.KING, not board.turn)) * king_value
        return material_value - material_value_enemy

    def feature_piecesquare_value(self, board: chess.Board):  # gevonden online -> kunnen het nog verbeteren
        if self.endGame:
            kings_table = kings_table_endgame
        else:
            kings_table = kings_table_middlegame
        pawnsq = sum([pawn_table[i] for i in board.pieces(chess.PAWN, board.turn)])
        pawnsq += sum([-pawn_table[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, not board.turn)])
        knightsq = sum([knights_table[i] for i in board.pieces(chess.KNIGHT, board.turn)])
        knightsq += sum([-knights_table[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, not board.turn)])
        bishopsq = sum([bishops_table[i] for i in board.pieces(chess.BISHOP, board.turn)])
        bishopsq += sum([-bishops_table[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, not board.turn)])
        rooksq = sum([rooks_table[i] for i in board.pieces(chess.ROOK, board.turn)])
        rooksq += sum([-rooks_table[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, not board.turn)])
        queensq = sum([queens_table[i] for i in board.pieces(chess.QUEEN, board.turn)])
        queensq += sum([-queens_table[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, not board.turn)])
        kingsq = sum([kings_table[i] for i in board.pieces(chess.KING, board.turn)])
        kingsq += sum([-kings_table[chess.square_mirror(i)] for i in board.pieces(chess.KING, not board.turn)])
        return pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

    def feature_mobility_value(self, board: chess.Board):
        mobility = 0
        for move in board.legal_moves:
            if board.piece_at(move.from_square).color == board.turn:
                mobility += 1
            else:
                mobility -= 1
        return mobility
