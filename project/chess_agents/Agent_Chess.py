import os

from project.chess_agents.agent import Agent
import chess

from project.chess_utilities.utility import Utility

import time
import random
import chess.syzygy #this is our book for endgames
import chess.polyglot

def openingSequence(board, book, isWhite) -> list[chess.Move]:
    moves = []
    move = None
    with chess.polyglot.open_reader(book) as openingMove:
        for entry in openingMove.find_all(board):
           moves.append(entry.move)
    if isWhite and moves:
        move = random.choice(moves)
    return move

def endGameSequence(board, endGameBook) -> list[chess.Move]:

   #https://www.chessprogramming.org/Syzygy_Bases
    with chess.syzygy.open_tablebase(endGameBook) as end:
        distanceZero = end.get_dtz(board) #to root the 50 move rule
        wdl = end.get_wdl(board) #win/ draw/ loss rate
    for moves in board.legal_moves:
        Capteruing = board.piece_at(moves.to_square)
        board.push(moves)
        with chess.syzygy.open.open_tablebase(endGameBook) as end: # open the endbook
            New_wdl = end.get_wdl(board)
            NewDistanceZero = end.get_dtz(board)

        board.pop();
        if wdl == 0:
            if New_wdl == -2:
                return moves
            elif New_wdl == -1 or New_wdl ==0:
                bestMove = moves
        if wdl ==1 or wdl ==2:
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
        self.whiteBook = whiteBook
        self.blackBook = blackBook
        self.endGameBook = endGameBook
        self.score: float = 0
        self.weightVector: dict = {}
        self.gameOpened: bool = False
        self.endGame: bool = False

        self.moveQueue: list = []

    def calculate_move(self, board: chess.Board) -> chess.Move:
        # Start timer
        start_time = time.time()  # Max 15 seconds

        # Check if there are moves queued
        if self.moveQueue:
            return self.moveQueue.pop()  # Pop the next action


        # Check begin game
        if not self.gameOpened:  # If game has not opened
            if isWhite:  # White opening
                self.moveQueue = openingSequence(board=chess.Board, book=self.whiteBook,isWhite= isWhite)
            else:  # Black opening
                self.moveQueue = openingSequence(board=chess.Board, book=self.blackBook,isWhite= isWhite)
            self.gameOpened = True
            return self.moveQueue.pop()

        # If endgame
        if not self.endGame:
            if sum(board.piece_map()) <= 8:  # Check for endgame
                self.moveQueue = endGameSequence(board=chess.Board, endGameBook=self.endGameBook)
                self.endGame = True

                return self.moveQueue.pop()

        # Else, start search
        optimal_move = self.negamax_heuristic_alpha_beta_prune()
        print("Move found in: " + str(start_time - time.time()))
        return optimal_move  # ?

    def negamax_heuristic_alpha_beta_prune(self, alpha: float, beta: float, depthleft: int, board: chess.Board, time_limit_move: float) -> float:
        """
        :param alpha:
        :param beta:
        :param depthLeft:
        :param board:
        :param time_limit_move:
        :return:
        """
        if depthleft == 0:  # TODO Or timelimiet
            return self.quiescence(alpha, beta, board)
        for move in board.legal_moves:
          score = -self.negamax_heuristic_alpha_beta_prune(-beta, -alpha, depthleft - 1, board)
          if score >= beta:
             return beta
          if score > alpha:
             alpha = score
        return alpha


    def quiescence(self, alpha, beta, board: chess.Board) -> float:
        """
        Quiescence uses a non-Linear Heuristic to approximate board value


        :param alpha:
        :param beta:
        :param board:
        """
        # TODO
        #if depthleft == 0:
        #    return self.quiescence(alpha, beta)
        for move in board.legal_moves:
            score = -self.negamax_heuristic_alpha_beta_prune(-beta, -alpha, depthLeft - 1, board)
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha
