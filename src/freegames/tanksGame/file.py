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
    def parseControls(controlString):
        controls = {}
        if controlString:
            for mapping in controlString.split(","):
                action, key = mapping.split(":")
                controls[action.strip()] = key.strip()
        return controls

    @staticmethod
    def loadSettingsAndMapFromFile(filePath):
        def parseInt(fileConfig, section, key, default=None, required=False):
            try:
                return int(fileConfig[section].get(key, default))
            except KeyError:
                if required:
                    raise KeyError(f"Missing key '{key}' in section '{section}'.")
                return default
            except ValueError:
                raise ValueError(f"Invalid integer value for '{key}' in section '{section}'.")
        if not os.path.exists(filePath):
            raise ValueError(f"The file '{filePath}' does not exist.")
        config = configparser.ConfigParser()
        config.read(filePath)
        requiredSections = ['map', 'settings', 'controls', 'filePaths', 'positions', 'enemies', 'bonuses']
        missingSections = [section for section in requiredSections if section not in config]
        if missingSections:
            raise ValueError(f"The configuration file is missing required sections: {', '.join(missingSections)}.")
        # Parse map
        try:
            tilesUnprocessed = config['map']['tiles']
            if not tilesUnprocessed:
                raise ValueError("The 'tiles' value in the 'map' section is empty.")
            tilesProcessed = tilesUnprocessed.replace(" ", "1")
            tileRows = [list(map(int, row.split(','))) for row in tilesProcessed.strip().splitlines()]
            flatTiles = [tile for row in tileRows for tile in row]
        except KeyError:
            raise KeyError("The 'tiles' key is missing in the 'map' section.")
        except ValueError as e:
            raise ValueError(f"Error processing tile data: {e}")
        # Parse settings
        rowsCount = parseInt(config, 'settings', 'rows', default='20')
        columnsCount = parseInt(config, 'settings', 'columns', default='20')
        tileSize = parseInt(config, 'settings', 'tileSize', default='20')
        startGameX = parseInt(config, 'settings', 'startGameX', default='500')
        startGameY = parseInt(config, 'settings', 'startGameY', default='100')
        basicHp = parseInt(config, 'settings', 'basicHp', default='3')
        basicAttack = parseInt(config, 'settings', 'basicAttack', default='1')
        numberOfRandomMines = parseInt(config, 'settings', 'numberOfRandomMines', default='0')
        timeAfterWhichMinesHide = parseInt(config, 'settings', 'timeAfterWhichMinesHide', default='10')
        # Parse controls
        firstTankControls = File.parseControls(config['controls'].get('firstTankControls', ''))
        secondTankControls = File.parseControls(config['controls'].get('secondTankControls', ''))
        # Parse file paths
        hallOfFameStoragePath = config['filePaths'].get('hallOfFameStoragePath', '')
        helpFilePath = config['filePaths'].get('helpFilePath', '')
        # Parse positions
        firstTankIndex = parseInt(config, 'positions', 'firstTankSpawnPosition', default='187')
        secondTankIndex = parseInt(config, 'positions', 'secondTankSpawnPosition', default='-1')
        # Parse enemies
        try:
            enemies = list(map(int, config['enemies']['enemyTanksPositions'].split(','))) if 'enemies' in config and 'enemyTanksPositions' in config['enemies'] else []
        except ValueError as e:
            raise ValueError(f"Invalid value in 'enemies' section: {e}.")
        # Parse bonuses
        try:
            enableBonuses = config['bonuses'].get('enableBonuses', 'true').lower() in ['true', '1', 'yes']
        except KeyError as e:
            raise KeyError(f"Missing key in 'bonuses' section: {e}.")
        except ValueError as e:
            raise ValueError(f"Invalid value in 'bonuses' section: {e}.")
        bonusSpawningFrequency = parseInt(config, 'bonuses', 'bonusSpawningFrequency', default='30')
        maxNumberOfBonuses = parseInt(config, 'bonuses', 'maxNumberOfBonuses', default='5')
        # Validate map size
        if rowsCount * columnsCount != len(flatTiles):
            raise ValueError(f"Invalid map size. Expected {rowsCount * columnsCount} tiles, but found {len(flatTiles)}.")
        if firstTankIndex >= len(flatTiles):
            raise ValueError(f"First tank spawn position index {firstTankIndex} is out of bounds (max: {len(flatTiles) - 1}).")
        if secondTankIndex >= len(flatTiles):
            raise ValueError(f"Second tank spawn position index {secondTankIndex} is out of bounds (max: {len(flatTiles) - 1}).")
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
            "secondTankControls": secondTankControls,
            "enableBonuses": enableBonuses,
            "bonusSpawningFrequency": bonusSpawningFrequency,
            "maxNumberOfBonuses": maxNumberOfBonuses
        }
