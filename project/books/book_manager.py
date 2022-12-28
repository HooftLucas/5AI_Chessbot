import random
import os

import chess
import chess.syzygy  # this is our book for endgames
import chess.polyglot

class BookManager:
    def __init__(self):
        self.startWhite = os.path.join(os.path.dirname(__file__), '../books/baron30.bin')
        self.endGameBook = os.path.join(os.path.dirname(__file__), '../books/syzygy')
        self.startBlack = os.path.join(os.path.dirname(__file__), '../books/Human.bin')

    def openingSequence(self, board: chess.Board, isWhite: bool) -> list[chess.Move]:
        moves = []
        move = None
        with chess.polyglot.open_reader(self.startWhite) as openingMove:
            for entry in openingMove.find_all(board):
                moves.append(entry.move)
        if isWhite and moves:
            move = random.choice(moves)
        return move

    def endGameSequence(self, board: chess.Board) -> list[chess.Move]:
        # https://www.chessprogramming.org/Syzygy_Bases
        with chess.syzygy.open_tablebase(self.endGameBook) as end:
            distanceZero = end.get_dtz(board)  # to root the 50 move rule
            wdl = end.get_wdl(board)  # win/ draw/ loss rate
        for moves in board.legal_moves:
            Capteruing = board.piece_at(moves.to_square)
            board.push(moves)
            with chess.syzygy.open.open_tablebase(self.endGameBook) as end:  # open the endbook
                New_wdl = end.get_wdl(board)
                NewDistanceZero = end.get_dtz(board)

            board.pop()
            if wdl == 0:
                if New_wdl == -2:
                    return moves
                elif New_wdl == -1 or New_wdl == 0:
                    bestMove = moves
            if wdl == 1 or wdl == 2:
                if New_wdl == -2 or New_wdl == -1:
                    if Capteruing:
                        return moves
                    else:
                        if abs(NewDistanceZero) <= abs(distanceZero):
                            distanceZero = NewDistanceZero
                            bestMove = moves
                if New_wdl == -1 or New_wdl == -2:
                    if New_wdl == -2 or New_wdl == -1 or New_wdl == 0:
                        return moves
                    else:
                        if abs(NewDistanceZero) >= abs(distanceZero):
                            distanceZero = NewDistanceZero
                            bestMove = moves
        return bestMove
