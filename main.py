import os
import sys
from src import Game
from src import tileColors, defaultTiles


def resourcePath(relative_path):
    if getattr(sys, 'frozen', False):  # If the app is frozen by PyInstaller
        base_path = os.path.dirname(sys.executable)  # Directory of main.exe
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Directory of main.py
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    BASE_DIR = resourcePath(".")
    CONFIG_FILE_PATH = resourcePath(os.path.join("settings", "game-config.ini"))
    sys.path.append(BASE_DIR)

    Game(defaultTiles, tileColors, CONFIG_FILE_PATH, BASE_DIR)
