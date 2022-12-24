from project.chess_agents.agent import Agent
import chess
from project.chess_utilities.utility import Utility
import time
from project.books.book_manager import BookManager

class ChessAgent(Agent):
    # We initialize the agent
    def __init__(self, utility: Utility, time_limit_move: float) -> None:
        super().__init__(utility, time_limit_move)
        self.name = "Intelligent chess agent"
        self.author = "Authors"

        # Books
        self.bookManager = BookManager()

        # Movement Queue
        self.moveQueue: list = []

        # States
        self.gameOpened: bool = True

        # Time related
        self.timeStart = 0
        self.maxTimePerMove = 15.0

        # Search Parameters
        self.iterative_deepening_depth: int = 3

        # Transposition table
        self.transpositionTable: dict[int, tuple[float, chess.Move]] = {}

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


        sortedMoves = self.iterative_deepening(board)

        # We now set up our starting values for the end result
        bestMove: chess.Move = sortedMoves[0]
        board.push(move=sortedMoves[0])
        alpha: float = self.utility.calculate_heuristic(board)
        beta = -alpha
        board.pop()
        """Once we have sorted our possible moves with iterative search, we explore further with alpha beta pruning"""
        for move in sortedMoves[1:]:
            board.push(move)
            boardScore = self.alphaBetaMax(board, alpha, beta, 50)
            board.pop()

            if boardScore > alpha:
                alpha = boardScore
                bestMove = move

        if board.is_irreversible(bestMove):  # If the move is reversible, we clear out the transposition table because earlier entries are not valid anymore
            self.transpositionTable.clear()
        return bestMove

    def iterative_deepening(self, board: chess.Board) -> list[chess.Move]:
        legalMoves: list[chess.Move] = list(board.legal_moves)
        moveScores: list[float] = [-100000] * len(legalMoves)

        for depth in range(self.iterative_deepening_depth):
            if depth == self.iterative_deepening_depth or time.time() - self.time_start > self.time_limit_move/5:
                break
            for moveIndex, move in enumerate(legalMoves):
                alpha = -100000
                beta = 100000
                board.push(move)
                moveScore = self.alphaBetaMax(board, alpha, beta, depth)
                board.pop()
                if moveScore > moveScores[moveIndex]:
                    moveScores[moveIndex] = moveScore

        sortedMoves = [move for _, move in sorted(zip(moveScores, legalMoves), key=lambda pair: pair[0])]
        return sortedMoves

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
        bestScore = -999999999999  # We need this to make sure alpha en beta
        bestMove: chess.Move = chess.Move.null()

        if depthLeft == 0 or time.time() - self.time_start > self.time_limit_move:
            return self.quiescence(board, alpha, beta)

        for move in board.legal_moves:
            board.push(move)
            boardValue = self.alphaBetaMax(board=board, alpha=-beta, beta=-alpha, depthLeft=depthLeft-1)
            board.pop()

            if boardValue >= beta:
                return boardValue
            if boardValue > bestScore:
                bestScore = boardValue
                bestMove = move
                if bestScore > alpha:
                    alpha = boardValue

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
                boardScore = -self.quiescence(board, -beta, -alpha)
                board.pop()
                if boardScore >= beta:
                    return beta
                if boardScore > alpha:
                    alpha = boardScore
        return alpha

