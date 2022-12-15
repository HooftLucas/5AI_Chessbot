#!/usr/bin/python3
import os

from project.chess_agents.Agent_Chess import Agent_Chess
from project.chess_engines.uci_engine import UciEngine
import chess
from project.chess_agents.example_agent import ExampleAgent
from project.chess_utilities.Utilities_Chess import Utilities_Chess
from project.chess_utilities.example_utility import ExampleUtility

if __name__ == "__main__":
    StartWhite = os.path.join('../books/baron30.bin');
    endGameBook = os.path.join('../books/syzygy');
    StartBlack = os.path.join('../books/Human.bin')
    # Create your utility
    utility = Utilities_Chess()
    # Create your agent
    agent = ExampleAgent(utility, 5.0)
    # Create the engine
    engine = UciEngine("engine", "Lucas, Robbe en Warre", agent)
    # Run the engine (will loop until the game is done or exited)
    engine.engine_operation()
