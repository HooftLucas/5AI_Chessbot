#!/usr/bin/python3
import os

from project.chess_agents.Agent_Chess import Agent_Chess
from project.chess_engines.uci_engine import UciEngine
import chess
from project.chess_agents.example_agent import ExampleAgent
from project.chess_utilities.Utilities_Chess import UtilitiesChess
from project.chess_utilities.example_utility import ExampleUtility

if __name__ == "__main__":
    StartWhite = os.path.join(os.path.dirname(__file__), '../books/baron30.bin')
    endGameBook = os.path.join(os.path.dirname(__file__), '../books/syzygy')
    StartBlack = os.path.join(os.path.dirname(__file__), '../books/Human.bin')
    print("leest de boeken")
    # Create your utility
    utility = UtilitiesChess({})
    # Create your agent
    agent = Agent_Chess(utility, 15.0, StartWhite, StartBlack, endGameBook)
    # Create the engine
    engine = UciEngine("engine2", "LRW", agent)
    # Run the engine (will loop until the game is done or exited)
    engine.engine_operation()
