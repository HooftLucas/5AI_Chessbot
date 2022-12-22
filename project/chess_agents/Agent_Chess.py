import random

from project.chess_agents.agent import Agent
import chess

from project.chess_utilities.utility import Utility

import time
import chess.syzygy  # this is our book for endgames
import chess.polyglot
def openingSequence(board, book) -> list[chess.Move]:
    moves = []
    move = None
    print("open with openingMove")
    with chess.polyglot.open_reader(book) as openingMove:
        for entry in openingMove.find_all(board):
            moves.append(entry.move)
    if moves: # later kunnen we dit nog specificieren als er met zwart of wit wordt gespeeld
        move = random.choice(moves)
    return move
def endGameSequence(board, endGameBook) -> chess.Move:
    bestMove = []
    # https://www.chessprogramming.org/Syzygy_Bases
    with chess.syzygy.open_tablebase(endGameBook) as end:
        distanceZero = end.get_dtz(board)  # to root the 50 move rule
        wdl = end.get_wdl(board)  # win/ draw/ loss rate
    for moves in board.legal_moves:
        Capteruing = board.piece_at(moves.to_square)
        board.push(moves)
        with chess.syzygy.open_tablebase(endGameBook) as end:  # open the endbook
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

class Agent_Chess(Agent):
    # Initialize your agent with whatever parameters you want
    def __init__(self, utility: Utility, time_limit_move: float, whiteBook, blackBook, endGameBook) -> None:
        super().__init__(utility, time_limit_move)
        self.name = "Search Agent"
        self.author = "Lucas, Robbe en Warre"
        self.moveQueue: list[chess.Move] = []
        self.time_start = 0
        self.whiteBook = whiteBook
        self.blackBook = blackBook
        self.endGameBook = endGameBook
        self.gameOpened: bool = False
        self.endGame: bool = True

    def calculate_move(self, board: chess.Board) -> chess.Move:
        self.time_start = time.time()
        isWhite: bool = board.turn == chess.WHITE

        if not self.gameOpened:  # If game has not opened

            if isWhite:  # White opening
               Move = openingSequence(board=board, book=self.whiteBook)
            else:  # Black opening
                Move = openingSequence(board=board, book=self.blackBook)
            self.gameOpened = True

            self.moveQueue.append(Move)
            board.push(self.moveQueue[0])
            return self.moveQueue.pop()
        # If endgame
        else:
            scoreTopBranches = self.iterative_deepening(3.0, board, 3)
            print(scoreTopBranches)
            moveTopBranches = [move for move in board.legal_moves]
            bestScore = -99999
            bestMove = chess.Move.null()
            alpha = -100000
            beta = 100000
            for move in moveTopBranches:
                board.push(move)
                score = -self.negamax_heuristic_alpha_beta_prune(beta=-beta, alpha=-alpha, depthleft=50, board=board)
                if score > bestScore:
                    bestScore = score
                    bestMove = move
                if score > alpha:
                    alpha = score
                board.pop()

            self.moveQueue.append(bestMove)
            board.push(self.moveQueue[0])
            return self.moveQueue.pop()

    def iterative_deepening(self, iterative_time_limit: float, board: chess.Board, maxDepth: int) -> list[float]:
        searchResult: list[float] = []
        Depth = 2
        alpha = -100000
        beta = 100000
        validMoves = [move for move in board.legal_moves]

        while time.time() < (iterative_time_limit + self.time_start) and Depth < 8:
            if time.time() - self.time_start > self.time_limit_move:
                break
            move: chess.Move = validMoves.pop()  # Take a valid move off the list

            board.push(move)
            moveScore = -self.negamax_heuristic_alpha_beta_prune(alpha=-alpha, beta=-beta, depthleft=Depth,
                                                                 board=board)  # Calculate the score in this branch

            board.pop()
            searchResult.append(moveScore)
            Depth += 1


        return searchResult

    def negamax_heuristic_alpha_beta_prune(self, alpha: float, beta: float,
                                           depthleft: int, board: chess.Board
                                           ) -> float:
        best_score = -99999
        if depthleft == 0 and time.time() - self.time_start < self.time_limit_move:
            return self.quiescence(alpha, beta, board)
        for move in board.legal_moves:
            if time.time() - self.time_start > self.time_limit_move:
                break
            board.push(move)

            score = -self.negamax_heuristic_alpha_beta_prune(beta=-beta, alpha=-alpha, depthleft=depthleft - 1,
                                                             board=board)
            board.pop()
            if score >= beta:
                return score
            if score > best_score:
                best_score = score
            if score > alpha:
                alpha = score
        return best_score

    def quiescence(self, alpha, beta, board: chess.Board) -> float:
        """
        Quiescence uses a non-Linear Heuristic to approximate board value

        :param alpha:
        :param beta:
        :param board:
        :return:
        """
        #print("quiescene")
        # First, check if we have already computed this state's score

        # If the score has not been computed, store it in the table
        score = self.utility.board_heuristic(board)

        # If the score is not optimal, return beta
        if score >= beta:
            return score
        if score > alpha:
            alpha = score

        # If we can explore more fully, open the moves
        for move in board.legal_moves:
            if time.time() - self.time_start > self.time_limit_move:
                break
            board.push(move)
            currentBoardScore = -self.quiescence(-alpha, -beta, board)
            board.pop()

            if currentBoardScore >= beta:
                return beta
            if currentBoardScore > alpha:
                alpha = currentBoardScore

        # Store the max calculated score to avoid extra computation
        return alpha