#!/usr/bin/python3
import os

from project.chess_agents.Agent_Chess import ChessAgent
from project.chess_engines.uci_engine import UciEngine
import chess
from project.chess_agents.example_agent import ExampleAgent
from project.chess_utilities.Utilities_Chess import ChessUtility
from project.chess_utilities.example_utility import ExampleUtility

if __name__ == "__main__":
    # Create your utility
    utility = ChessUtility([1, 1, 1, 1])
    # Create your agent
    agent = ChessAgent(utility, 15.0)
    # Create the engine
    engine = UciEngine("engine2", "LRW", agent)
    # Run the engine (will loop until the game is done or exited)
    engine.engine_operation()
