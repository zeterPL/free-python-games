import os
import sys
from src import Game
from src import tileColors, defaultTiles

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings", "game-config.ini")
    sys.path.append(BASE_DIR)

    Game(defaultTiles, tileColors, CONFIG_FILE_PATH, BASE_DIR)