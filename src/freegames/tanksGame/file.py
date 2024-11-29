import configparser
import os


class File:
    @staticmethod
    def loadFileAsArray(filename, errorMessage="There was a problem loading file content"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return file.readlines()
        except FileNotFoundError:
            print(f"{errorMessage} File {filename} not found")
            return [errorMessage]

    @staticmethod
    def parseControls(control_string):
        controls = {}
        for mapping in control_string.split(","):
            action, key = mapping.split(":")
            controls[action.strip()] = key.strip()
        return controls

    @staticmethod
    def loadSettingsAndMapFromFile(filePath):
        if not os.path.exists(filePath):
            raise ValueError(f"The file '{filePath}' does not exist.")
        config = configparser.ConfigParser()
        config.read(filePath)
        requiredSections = ['map', 'settings', 'controls', 'positions']
        if not all(section in config for section in requiredSections):
            raise ValueError(f"The configuration file must have {requiredSections} sections.")
        tilesUnprocessed = config['map']['tiles']
        if not tilesUnprocessed:
            raise ValueError("No tiles found in the 'map' section of the configuration file.")
        try:
            tilesProcessed = tilesUnprocessed.replace(" ", "1")
            tileRows = [list(map(int, row.split(','))) for row in tilesProcessed.strip().splitlines()]
            flatTiles = [tile for row in tileRows for tile in row]
        except ValueError as e:
            raise ValueError(f"Error processing tile data: {e}")
        try:
            rowsCount = int(config['settings'].get('rows', '20'))
            columnsCount = int(config['settings'].get('columns', '20'))
            tileSize = int(config['settings'].get('tileSize'))
            startGameX = int(config['settings'].get('startGameX'))
            startGameY = int(config['settings'].get('startGameY'))
            basicHp = int(config['settings'].get('basicHp', '3'))
            basicAttack = int(config['settings'].get('basicAttack', '1'))
            numberOfRandomMines = int(config['settings'].get('numberOfRandomMines', '0'))
            timeAfterWhichMinesHide = int(config['settings'].get('timeAfterWhichMinesHide', '10'))
            firstTankIndex = int(config['positions'].get('firstTankSpawnPosition', '187'))
            secondTankIndex = int(config['positions'].get('secondTankSpawnPosition', '-1'))
            enemies = list(map(int, config['enemies']['enemyTanksPositions'].split(','))) if 'enemies' in config and 'enemyTanksPositions' in config['enemies'] else []
            hallOfFameStoragePath = config['filePaths']['hallOfFameStoragePath'] if 'filePaths' in config and 'hallOfFameStoragePath' in config['filePaths'] else 'files/hallOfFame.txt'
            helpFilePath = config['filePaths']['helpFilePath'] if 'filePaths' in config and 'helpFilePath' in config['filePaths'] else 'files/help.txt'
            firstTankControls = File.parseControls(config['controls'].get('firstTankControls', ''))
            secondTankControls = File.parseControls(config['controls'].get('secondTankControls', ''))
        except ValueError as e:
            raise ValueError(f"Error reading settings: {e}")
        if rowsCount * columnsCount != len(flatTiles):
            raise ValueError(f"Invalid map size compare to settings. Map have {len(flatTiles)} tiles, but settings have {rowsCount}x{columnsCount}={rowsCount * columnsCount}.")
        if firstTankIndex > len(flatTiles):
            raise ValueError(f"Invalid first tank spawn position. Tank index {firstTankIndex} out of range. Max possible {len(flatTiles) - 1} index.")
        if secondTankIndex > len(flatTiles):
            raise ValueError(f"Invalid second tank spawn position. Tank index {secondTankIndex} out of range. Max possible {len(flatTiles) - 1} index.")
        return {
            "map": flatTiles,
            "rows": rowsCount,
            "columns": columnsCount,
            "tileSize": tileSize,
            "startGameX": startGameX,
            "startGameY": startGameY,
            "basicHp": basicHp,
            "basicAttack": basicAttack,
            "firstTankIndex": firstTankIndex,
            "numberOfRandomMines": numberOfRandomMines,
            "timeAfterWhichMinesHide": timeAfterWhichMinesHide,
            "secondTankIndex": secondTankIndex,
            "enemies": enemies,
            "hallOfFameStoragePath": hallOfFameStoragePath,
            "helpFilePath": helpFilePath,
            "firstTankControls": firstTankControls,
            "secondTankControls": secondTankControls
        }
