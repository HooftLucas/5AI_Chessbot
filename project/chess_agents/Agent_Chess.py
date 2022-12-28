from project.chess_agents.agent import Agent
import chess
from project.chess_utilities.utility import Utility
import time
from project.books.book_manager import BookManager

class ChessAgent(Agent):
    # We initialize the agent
    def __init__(self, utility: Utility, time_limit_move: float) -> None:
        super().__init__(utility, time_limit_move)
        self.name = "Big brain chess agent"
        self.author = "Lukas, Robbe en Warre"

        self.bookManager = BookManager()
        self.moveQueue: list = []

        # States
        self.gameOpened: bool = True
        self.time_start = 0

        # Search Parameters
        self.iterative_deepening_depth: int = 6

        self.transpositionTable = {}

    def calculate_move(self, board: chess.Board):
        self.time_start = time.time()
        print("Starting ...")

        # Check if we have any moves in Queue
        if self.moveQueue:
            board.push(move=self.moveQueue[0])
            return self.moveQueue.pop()

        # Check begin game
        if not self.gameOpened:  # If game has not opened
            if board.turn == chess.WHITE:  # White opening
                self.moveQueue = self.bookManager.openingSequence(board=board, isWhite=True)
            else:  # Black opening
                self.moveQueue = self.bookManager.openingSequence(board=board, isWhite=True)
            self.gameOpened = True
            return self.moveQueue.pop()

        # If endgame
        if sum(board.piece_map()) <= 7:  # Check for endgame
            self.moveQueue = self.bookManager.endGameSequence(board=board)
            self.utility.set_end_game()
            board.push(self.moveQueue[0])
            return self.moveQueue.pop()

        move = self.iterative_deepening(board)

        if board.is_irreversible(move):
            self.transpositionTable.clear()
        return move

    def iterative_deepening(self, board: chess.Board) -> chess.Move:
        bestScore = -99999
        alpha = -100000
        beta = 100000
        bestMove = chess.Move.null()

        key = chess.polyglot.zobrist_hash(board)
        if key in self.transpositionTable:
            _, move = self.transpositionTable[key]
            return move

        stop = False
        for depth in range(self.iterative_deepening_depth):
            if stop: break
            for move in board.legal_moves:
                if time.time() - self.time_start > self.time_limit_move: # / 5:
                    stop = True
                    break
                board.push(move)
                moveScore = -self.alphaBetaMax(board, -beta, -alpha, depth)
                board.pop()
                if moveScore > bestScore:
                    bestScore = moveScore
                    bestMove  = move
                if moveScore > alpha:
                    alpha = moveScore

        if bestMove == chess.Move.null():
            return list(board.legal_moves)[0]

        self.transpositionTable[key] = (bestScore, bestMove)
        return bestMove

    def alphaBetaMax(self, board: chess.Board, alpha: float, beta: float, depthLeft: int) -> float:
        """

        :param board: current board state
        :param alpha: value for agent
        :param beta: value for opponent
        :param depthLeft: depth left to explore in the tree
        :return: returns the best score
        """
        key = chess.polyglot.zobrist_hash(board)  # Get the hash of the board (current position)
        if key in self.transpositionTable:
            moveScore, _ = self.transpositionTable[key]
            return moveScore
        bestScore = -99999
        bestMove: chess.Move = chess.Move.null()

        if depthLeft == 0:
            return self.quiescence(board, alpha, beta)

        for move in board.legal_moves:
            if time.time() - self.time_start > self.time_limit_move:
                break
            board.push(move)
            score = -self.alphaBetaMax(board, -beta, -alpha, depthLeft - 1)
            board.pop()
            if score >= beta:
                return score
            if score > bestScore:
                bestScore = score
                bestMove = move
            if score > alpha:
                alpha = score

        if bestMove != chess.Move.null():
            self.transpositionTable[key] = (bestScore, bestMove)
        return bestScore

    def quiescence(self, board: chess.Board, alpha: float, beta: float) -> float:
        # Combat the horizon effect, and look deeper at capture moves
        boardScore = self.utility.calculate_heuristic(board)
        if boardScore >= beta:
            return boardScore
        if alpha < boardScore:
            alpha = boardScore

        for move in board.legal_moves:
            if time.time() - self.time_start > self.time_limit_move:
                break
            if board.is_capture(move) or board.gives_check(move):
                board.push(move)
                score = -self.quiescence(board, -beta, -alpha)
                board.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha
