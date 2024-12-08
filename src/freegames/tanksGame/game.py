from turtle import Turtle, setup, hideturtle, listen, update, done, tracer, onkey, ontimer, bgcolor, clearscreen, resetscreen
from freegames import floor, vector
import os
from pygame import mixer
import random
from tkinter.simpledialog import askstring
from enum import Enum
from file import File
from tank import Tank
from aiTank import AITank
from bonus import Bonus
from tile import Tile, tileColors, defaultTiles
from draw import Draw
from bullet import Bullet


class GameMode(Enum):
    SINGLE = 0
    PVP = 1
    PVE = 2


class Game:
    def __init__(self, initialTiles, initialTileColors, settingsFile=None):
        self.hallOfFameStoragePath = ""
        self.helpFilePath = ""
        self.initialTiles = initialTiles
        self.rows = 20
        self.columns = 20
        self.tileSize = 20
        self.startGameX = 500
        self.startGameY = 100
        self.basicHp = 3
        self.basicAttack = 1
        self.numberOfRandomMines = 0
        self.timeAfterWhichMinesHide = 10
        self.firstTankSpawnIndex = 187
        self.secondTankSpawnIndex = None
        self.enemyTanksSpawnIndexes = []
        self.firstTankControls = {'Up': 'Up', 'Down': 'Down', 'Left': 'Left', 'Right': 'Right', 'Stop': 'Control_R', 'Shoot': 'Return'}
        self.secondTankControls = {'Up': 'w', 'Down': 's', 'Left': 'a', 'Right': 'd', 'Stop': 'Control_L', 'Shoot': 'Shift_L'}
        self.enableBonuses = False
        self.bonusSpawningFrequency = 10
        self.maxNumberOfBonuses = 3
        self.assignSettingsFromFile(settingsFile)
        self.tiles = list(self.initialTiles)
        self.tileColors = initialTileColors
        self.gameWidth = self.columns * self.tileSize
        self.gameHeight = self.rows * self.tileSize
        self.helpContent = File.loadFileAsArray(self.helpFilePath, "There was a problem loading help content.") if self.helpFilePath else None

        self.mapTurtle = Turtle(visible=False)
        self.messageTurtle = Turtle(visible=False)
        self.minesTurtle = Turtle(visible=False)

        self.gameRunning = False
        self.gamePaused = False
        self.roundCounter = 0
        self.gameMode = None

        self.firstTank = None
        self.secondTank = None
        self.enemyTanks = []
        self.occupiedTilesByEnemies = {}
        self.allTanks = []
        self.bullets = []
        self.bonuses = []

        self.tankCentralization = self.tileSize // 10  # minimal shift of tanks to make tanks stay in the center of the title
        self.tankSpeedValue = self.tileSize // 4
        self.controls1 = {
            self.firstTankControls['Up']: (vector(0, self.tankSpeedValue), 0),
            self.firstTankControls['Down']: (vector(0, -self.tankSpeedValue), 180),
            self.firstTankControls['Left']: (vector(-self.tankSpeedValue, 0), 270),
            self.firstTankControls['Right']: (vector(self.tankSpeedValue, 0), 90)
        }
        self.controls2 = {
            self.secondTankControls['Up']: (vector(0, self.tankSpeedValue), 0),
            self.secondTankControls['Down']: (vector(0, -self.tankSpeedValue), 180),
            self.secondTankControls['Left']: (vector(-self.tankSpeedValue, 0), 270),
            self.secondTankControls['Right']: (vector(self.tankSpeedValue, 0), 90)
        }

        mixer.init()  # for playing sounds
        self.laserShootSound = mixer.Sound("files/sounds/laserShoot.wav")
        self.explosionSound = mixer.Sound("files/sounds/explosion.wav")
        self.damageSound = mixer.Sound("files/sounds/damage.wav")
        self.gameOverSound = mixer.Sound("files/sounds/game-over.mp3")
        self.victorySound = mixer.Sound("files/sounds/victory.mp3")

        self.modalWidth, self.modalHeight = 400, 300
        self.showStartMenu()
        done()

    def assignSettingsFromFile(self, settingsFile):
        if not settingsFile:
            return
        try:
            loadedData = File.loadSettingsAndMapFromFile(settingsFile)
            self.initialTiles = loadedData['map'] or self.initialTiles
            self.rows = loadedData['rows'] or self.rows
            self.columns = loadedData['columns'] or self.columns
            self.tileSize = loadedData['tileSize'] or self.tileSize
            self.startGameX = loadedData['startGameX'] if loadedData['startGameX'] is not None else self.startGameX
            self.startGameY = loadedData['startGameY'] if loadedData['startGameY'] is not None else self.startGameY
            self.basicHp = loadedData['basicHp'] or self.basicHp
            self.basicAttack = loadedData['basicAttack'] or self.basicAttack
            self.numberOfRandomMines = loadedData['numberOfRandomMines'] if loadedData['numberOfRandomMines'] is not None else self.numberOfRandomMines
            self.timeAfterWhichMinesHide = loadedData['timeAfterWhichMinesHide'] if loadedData['timeAfterWhichMinesHide'] is not None else self.timeAfterWhichMinesHide
            self.firstTankSpawnIndex = loadedData['firstTankIndex'] if loadedData['firstTankIndex'] is not None else self.firstTankSpawnIndex
            self.secondTankSpawnIndex = loadedData['secondTankIndex'] if loadedData['secondTankIndex'] != -1 else None
            self.enemyTanksSpawnIndexes = loadedData['enemies'] or self.enemyTanksSpawnIndexes
            self.hallOfFameStoragePath = loadedData.get("hallOfFameStoragePath", self.hallOfFameStoragePath)
            self.helpFilePath = loadedData.get('helpFilePath', self.helpFilePath)
            self.firstTankControls = loadedData['firstTankControls'] or self.firstTankControls
            self.secondTankControls = loadedData['secondTankControls'] or self.secondTankControls
            self.enableBonuses = loadedData.get('enableBonuses', self.enableBonuses)
            self.bonusSpawningFrequency = loadedData.get('bonusSpawningFrequency', self.bonusSpawningFrequency)
            self.maxNumberOfBonuses = loadedData.get('maxNumberOfBonuses', self.maxNumberOfBonuses)
            print(f"Map and settings successfully loaded from '{settingsFile}'!")
        except ValueError as e:
            print(f"Error loading configuration: {e}")
            exit()

    def getTilePosition(self, index):
        x = (index % self.columns) * self.tileSize - (self.columns // 2) * self.tileSize
        y = (self.rows // 2 - 1) * self.tileSize - (index // self.columns) * self.tileSize
        return x, y

    def getTileIndexFromPoint(self, point):
        x = (floor(point.x, self.tileSize, self.tileSize * (self.columns // 2)) + (self.columns // 2) * self.tileSize) / self.tileSize
        y = ((self.rows // 2 - 1) * self.tileSize - floor(point.y, self.tileSize, self.tileSize * (self.rows // 2))) / self.tileSize
        index = int(x + y * self.columns)
        return index

    def getNeighbors(self, index, validationFunction=lambda x: True):
        if index is None or not (0 <= index < self.rows * self.columns):
            return []
        neighbors = []
        row = index // self.columns
        column = index % self.columns
        if column > 0 and validationFunction(index - 1):
            neighbors.append(index - 1)
        if column < self.columns - 1 and validationFunction(index + 1):
            neighbors.append(index + 1)
        if row > 0 and validationFunction(index - self.columns):
            neighbors.append(index - self.columns)
        if row < self.rows - 1 and validationFunction(index + self.columns):
            neighbors.append(index + self.columns)
        return neighbors

    def valid(self, point):
        blockingTiles = [Tile.NO_TILE.value, Tile.RIVER.value, Tile.INDESTRUCTIBLE_BLOCK.value, Tile.DESTRUCTIBLE_BLOCK.value]
        index = self.getTileIndexFromPoint(point)
        if index >= len(self.tiles) or index < 0:
            print(f"Index out of range {index=} {point=}")
            return False
        if self.tiles[index] in blockingTiles:
            return False
        index = self.getTileIndexFromPoint(point + int(self.tileSize * 0.95) - self.tankCentralization)
        if self.tiles[index] in blockingTiles:
            return False
        return point.x % self.tileSize == self.tankCentralization or point.y % self.tileSize == self.tankCentralization

    def replaceBordersWithTeleport(self):
        replaceValues = [Tile.NO_TILE.value, Tile.ROAD.value, Tile.FOREST.value, Tile.DESTRUCTIBLE_BLOCK.value, Tile.DESTROYED_DESTRUCTIBLE_BLOCK, Tile.MINE.value]
        for col in range(self.columns):
            if self.tiles[col] in replaceValues:  # 1 row
                self.tiles[col] = Tile.TELEPORT.value
            if self.tiles[(self.rows - 1) * self.columns + col] in replaceValues:  # last row
                self.tiles[(self.rows - 1) * self.columns + col] = Tile.TELEPORT.value
        for row in range(self.rows):
            if self.tiles[row * self.columns] in replaceValues:  # 1 column
                self.tiles[row * self.columns] = Tile.TELEPORT.value
            if self.tiles[row * self.columns + self.columns - 1] in replaceValues:  # last column
                self.tiles[row * self.columns + self.columns - 1] = Tile.TELEPORT.value

    def spawnRandomMines(self):
        # get all occupied indexes by tanks
        occupiedIndexes = set(index for indexes in self.occupiedTilesByEnemies.values() for index in indexes)
        occupiedIndexes.update({self.firstTankSpawnIndex})
        if self.secondTankSpawnIndex is not None:
            occupiedIndexes.add(self.secondTankSpawnIndex)
        # add to occupiedIndexes theirs neighbors
        neighborsToOccupiedIndexes = set()
        for index in occupiedIndexes:
            neighborsToOccupiedIndexes.update(self.getNeighbors(index))
        occupiedIndexes.update(neighborsToOccupiedIndexes)
        # spawn mines in possible indexes
        possibleIndexes = [index for index, value in enumerate(self.tiles) if value == Tile.ROAD.value and index not in occupiedIndexes]
        for _ in range(self.numberOfRandomMines):
            if not possibleIndexes:  # Break if there are no valid positions left
                break
            randomIndex = random.choice(possibleIndexes)
            self.tiles[randomIndex] = 7
            possibleIndexes.remove(randomIndex)  # Prevent duplicate selection

    def startGame(self):
        if self.gameRunning:
            return

        self.roundCounter = 0
        self.gameRunning = True
        self.gamePaused = False
        self.tiles = list(self.initialTiles)  # restarting map to state before changes in game
        self.bullets = []
        self.enemyTanks = []
        self.allTanks = []
        self.bonuses = []

        setup(max((self.columns + 1) * self.tileSize, 420), max((self.rows + 1) * self.tileSize, 420), self.startGameX, self.startGameY)

        firstTankPosition = self.getTilePosition(self.firstTankSpawnIndex)
        self.firstTank = Tank(self, firstTankPosition[0] + self.tankCentralization, firstTankPosition[1] + self.tankCentralization, "dark green", 0,
                              self.controls1, self.firstTankControls['Stop'], self.firstTankControls['Shoot'])
        self.allTanks = [self.firstTank]

        if self.gameMode in [GameMode.PVP, GameMode.PVE]:
            if self.secondTankSpawnIndex:
                secondTankPosition = self.getTilePosition(self.secondTankSpawnIndex)
                self.secondTank = Tank(self, secondTankPosition[0] + self.tankCentralization, secondTankPosition[1] + self.tankCentralization, "slate gray", 1,
                                       self.controls2, self.secondTankControls['Stop'], self.secondTankControls['Shoot'])
                self.allTanks.append(self.secondTank)
        else:
            self.secondTank = None

        for enemyId, enemyTankSpawnIndex in enumerate(self.enemyTanksSpawnIndexes, 2):
            enemyTankPosition = self.getTilePosition(enemyTankSpawnIndex)
            enemyTank = AITank(self, enemyTankPosition[0] + self.tankCentralization, enemyTankPosition[1] + self.tankCentralization, "gold", enemyId, self.firstTank)
            self.enemyTanks.append(enemyTank)
        self.allTanks.extend(self.enemyTanks)

        self.replaceBordersWithTeleport()
        self.spawnRandomMines()
        self.drawBoard()
        self.roundOfMovement()

    def roundOfMovement(self):
        if self.gamePaused or not self.gameRunning:
            return
        for playerTank in list(set(self.allTanks) - set(self.enemyTanks)):
            playerTank.tankMovement()
            playerTank.moveTank()
        for enemyTank in self.enemyTanks:
            enemyTank.moveTank()
        Bullet.processBulletsMovementsAndCollisions(self)
        self.checkIfGameOver()
        update()
        if self.gameRunning:
            self.roundCounter += 1
            if self.roundCounter == self.timeAfterWhichMinesHide*10:
                self.minesTurtle.clear()
            if self.roundCounter % (self.bonusSpawningFrequency*10) == 0:  # every x seconds spawn new bonus
                Bonus.spawnBonus(self)
            if self.roundCounter % 10 == 0:  # every second update active bonuses statuses
                for tank in self.allTanks:
                    Bonus.updateActiveBonuses(tank)
            ontimer(self.roundOfMovement, 100)

    def checkIfGameOver(self):
        if self.gameMode == GameMode.SINGLE:
            if self.firstTank.destroyed:
                self.endGame(False, self.firstTank.deathReason)
            elif all(tank.destroyed for tank in self.enemyTanks):
                self.endGame(True, "All enemy tanks destroyed")
        elif self.gameMode == GameMode.PVP:
            if self.firstTank.destroyed:
                self.endGame(False, self.firstTank.deathReason)
            elif self.secondTank.destroyed:
                self.endGame(False, self.secondTank.deathReason)
        elif self.gameMode == GameMode.PVE:
            if self.firstTank.destroyed and self.secondTank.destroyed:
                self.endGame(False, "All players tanks destroyed")
            elif all(tank.destroyed for tank in self.enemyTanks):
                self.endGame(True, "All enemy tanks destroyed")

    def endGame(self, victory, announcement):
        self.gameRunning = False
        for tank in self.allTanks:  # draw destroyed tanks
            tank.drawTank()
        ontimer(lambda: self.conditionalExecution(not self.gameRunning, self.victorySound.play if victory else self.gameOverSound.play), 1000)
        ontimer(lambda: self.conditionalExecution(not self.gameRunning, self.drawModalMessage, f"{'Victory' if victory else 'Game Over'}!\n{announcement}", "Press 'R' to restart"), 2000)
        if self.gameMode == GameMode.SINGLE:
            ontimer(lambda: self.conditionalExecution(not self.gameRunning, lambda v=victory: self.initHallOfFame(v)), 2000)
        onkey(self.startGame, "r")

    @staticmethod
    def conditionalExecution(condition, function, *args, **kwargs):
        conditionResult = condition() if callable(condition) else condition
        if conditionResult:
            return function(*args, **kwargs)

    def tanksCollision(self, tankChecking, tankCheckingPosition=None, collisionThreshold=20):
        tankCheckingPosition = tankCheckingPosition or tankChecking.position
        for otherTank in self.allTanks:
            distanceBetweenTanks = abs(tankCheckingPosition - otherTank.position)
            if otherTank != tankChecking and distanceBetweenTanks < collisionThreshold and tankChecking.speed != vector(0, 0):
                if not otherTank.destroyed:  # to improve gameplay collision with destroyed tank won't take damage
                    tankChecking.takeDamage(1, f"tank {tankChecking.tankId} collide with tank {otherTank.tankId}")
                    otherTank.takeDamage(1, f"tank {otherTank.tankId} collide with tank {tankChecking.tankId}")
                tankChecking.speed = vector(0, 0)
                return True
        return False

    def togglePause(self):
        self.gamePaused = not self.gamePaused
        if not self.gamePaused:
            print("Game resumes!")
            self.messageTurtle.clear()
            self.roundOfMovement()
        else:
            print("Game paused!")
            self.drawModalMessage("Game Paused!", "Press 'P' to play")

    def toggleHelpMenu(self):
        if not self.helpContent:
            print("Help menu was not loaded correctly, so you can't open menu.")
            return
        self.gamePaused = not self.gamePaused
        if not self.gamePaused:
            self.messageTurtle.clear()
            if self.gameRunning:
                self.roundOfMovement()
            else:
                self.showStartMenu()
        else:
            self.showHelpMenu()

    @staticmethod
    def writeText(turtleObject, x, y, message, textAlign="center", textFont=("Arial", 16, "bold"), textColor="black"):
        turtleObject.color(textColor)
        turtleObject.goto(x, y)
        turtleObject.write(message, align=textAlign, font=textFont)

    def drawBoard(self):
        Draw.drawSquare(self.mapTurtle, -self.gameWidth, -self.gameHeight, 2 * (self.gameWidth + self.gameHeight), "black")
        bgcolor('black')
        for index in range(len(self.tiles)):
            tile = self.tiles[index]
            if tile > 0:
                x, y = self.getTilePosition(index)
                tileColor = self.tileColors[tile]
                Draw.drawSquare(self.mapTurtle, x, y, self.tileSize, squareColor=tileColor)
                if tile == Tile.MINE.value:  # drawing mines
                    Draw.drawCircle(self.minesTurtle, x + self.tileSize // 2, y + self.tileSize // 2, self.tileSize // 2, "black")
                if tile == Tile.TELEPORT.value:  # drawing portals
                    Draw.drawPortal(self.mapTurtle, x + self.tileSize // 2, y + self.tileSize // 2, self.tileSize * 0.8, 5, "purple", "black")
        Draw.drawRectangle(self.mapTurtle, 0, 0, self.rows * self.tileSize, self.columns * self.tileSize, "", "white", True)  # drawing white circuit around board

    def drawExplosion(self, drawingTurtle, x, y, explosionIteration=0, maxIterations=3):
        explosionColors = ["red", "yellow", "orange"]
        explosionColor = explosionColors[explosionIteration % len(explosionColors)]
        t = self.tileSize // 20
        offsets = [(0, 0), (2 * t, 2 * t), (-2 * t, -2 * t), (-2 * t, 2 * t), (2 * t, -2 * t), (4 * t, 0), (0, 4 * t), (-4 * t, 0), (0, -4 * t)]
        for dx, dy in offsets:
            Draw.drawSquare(drawingTurtle, x + dx * (explosionIteration + t), y + dy * (explosionIteration + t), 2 * t + explosionIteration, explosionColor)
        if explosionIteration < maxIterations:
            ontimer(lambda: self.drawExplosion(drawingTurtle, x, y, explosionIteration + 1, maxIterations), 150)
        else:
            ontimer(drawingTurtle.clear, 200)

    def drawModalMessage(self, message, subMessage, x=0, y=0, modalWidth=350, modalHeight=120):
        self.messageTurtle.clear()
        Draw.drawRectangle(self.messageTurtle, x, y, modalWidth, modalHeight, "white", "black", True)
        self.writeText(self.messageTurtle, 0, 0, message)
        self.writeText(self.messageTurtle, 0, -40, subMessage, textFont=("Arial", 12, "normal"))

    @staticmethod
    def resetGame():
        resetscreen()
        clearscreen()
        setup(420, 420, 540, 200)
        hideturtle()
        tracer(False)
        listen()

    def showStartMenu(self):
        self.gameRunning = False
        self.resetGame()
        Draw.drawRectangle(self.messageTurtle, 0, 0, self.modalWidth, self.modalHeight, "white", "black", True, borderThickness=2)
        self.writeText(self.messageTurtle, 0, 70, "Tank Battle Game", textFont=("Arial", 32, "bold"))
        self.writeText(self.messageTurtle, 0, -20, "Press 'P' to Play", textFont=("Arial", 18, "normal"))
        self.writeText(self.messageTurtle, 0, -60, "Press 'H' for Help", textFont=("Arial", 18, "normal"))
        self.writeText(self.messageTurtle, 0, -100, "Press Escape for Exit", textFont=("Arial", 18, "normal"))

        onkey(lambda: self.showGameModeMenu(), "p")
        onkey(lambda: self.toggleHelpMenu(), "h")
        onkey(lambda: exit(), "Escape")

    def setGameMode(self, mode):
        self.gameMode = mode
        self.startGame()
        onkey(lambda: self.togglePause(), "p")

    def showGameModeMenu(self):
        self.messageTurtle.clear()
        Draw.drawRectangle(self.messageTurtle, 0, 0, self.modalWidth, self.modalHeight, "white", "black", True, borderThickness=2)
        self.writeText(self.messageTurtle, 0, 100, "Select Game Mode", textFont=("Arial", 28, "bold"))
        self.writeText(self.messageTurtle, 0, 50, "Press '1' for Single Player", textFont=("Arial", 16, "normal"))
        self.writeText(self.messageTurtle, 0, 0, "Press '2' for PvP mode     ", textFont=("Arial", 16, "normal"))
        self.writeText(self.messageTurtle, 0, -50, "Press '3' for PvE mode     ", textFont=("Arial", 16, "normal"))
        self.writeText(self.messageTurtle, 0, -110, "Press 'H' for Help", textFont=("Arial", 12, "italic"))
        self.writeText(self.messageTurtle, 0, -140, "Press 'Escape' to return to Menu", textFont=("Arial", 12, "italic"))

        onkey(lambda: self.setGameMode(GameMode.SINGLE), "1")
        onkey(lambda: self.setGameMode(GameMode.PVP), "2")
        onkey(lambda: self.setGameMode(GameMode.PVE), "3")
        onkey(lambda: self.showStartMenu(), "Escape")

    def showHelpMenu(self, modalWidth=420, modalHeight=420):
        self.messageTurtle.clear()
        Draw.drawRectangle(self.messageTurtle, 0, 0, modalWidth, modalHeight, "white", "black", True)
        yOffset = (modalHeight / 2) - 40
        longestTextLineWidth = 312  # I checked manually how many pixels take to write the longest line
        for line in self.helpContent:
            strippedLine = line.lstrip()
            leadingSpaces = len(line) - len(strippedLine)
            xOffset = -modalWidth / 2 + (modalWidth - longestTextLineWidth) / 2
            xOffset += leadingSpaces * 10
            self.writeText(self.messageTurtle, xOffset, yOffset, line, "left", ("Arial", 10, "normal"))
            yOffset -= 20
        if self.gameRunning:
            self.writeText(self.messageTurtle, 0, yOffset - 10, "Press 'H' to return to the game", textFont=("Arial", 8, "italic"))
        else:
            self.writeText(self.messageTurtle, 0, yOffset - 10, "Press 'H' to return to the start menu", textFont=("Arial", 8, "italic"))

    def initHallOfFame(self, victory):
        if os.path.exists(self.hallOfFameStoragePath):
            score = int(len(self.enemyTanks) * (
                    (1000 if victory else 0) +
                    20 * self.basicHp * sum(1 for tank in self.enemyTanks if tank.destroyed) +
                    10 * sum(max(self.basicHp - tank.hp, 0) for tank in self.enemyTanks if not tank.destroyed) +
                    max(10 * self.firstTank.hp, 0)))
            playerName = askstring("Hall of Fame", "Enter your name:\t\t\t\t") or "Anonymous"
            self.saveToHallOfFame(playerName, score)
            self.showHallOfFame()

    def showHallOfFame(self, modalWidth=400, modalHeight=500):
        setup(max((self.columns + 1) * self.tileSize, 400), max((self.rows + 1) * self.tileSize, 500), self.startGameX, self.startGameY)
        scores = self.loadHallOfFame()
        self.messageTurtle.clear()
        Draw.drawRectangle(self.messageTurtle, 0, 0, modalWidth, modalHeight, "white", "black", True)
        self.writeText(self.messageTurtle, 0, 180, "🏆 Hall of Fame 🏆", textFont=("Arial", 32, "bold"))

        y_offset = 130
        for index, (name, score) in enumerate(scores, 1):
            resultTextFont = ("Arial", 24, "bold") if index <= 3 else ("Arial", 16, "normal")
            resultTextColor = "gold" if index == 1 else "silver" if index == 2 else "chocolate3" if index == 3 else "black"
            self.writeText(self.messageTurtle, -150, y_offset, f"{index}. {name} - {score}", "left", textFont=resultTextFont, textColor=resultTextColor)
            y_offset -= 35
        self.writeText(self.messageTurtle, 0, -220, "Press 'R' to restart", textFont=("Arial", 10, "italic"))

    def loadHallOfFame(self):
        with open(self.hallOfFameStoragePath, "r", encoding="utf-8") as file:
            lines = file.readlines()
        scores = []
        for line in lines:
            try:
                name, score = line.strip().split(":")
                scores.append((name, int(score)))
            except ValueError:
                continue
        return scores

    def saveToHallOfFame(self, name, score):
        scores = self.loadHallOfFame()
        found = False
        for i, (playerName, playerScore) in enumerate(scores):
            if playerName == name:
                scores[i] = (name, max(score, playerScore))
                found = True
                break
        if not found:
            scores.append((name, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        scores = scores[:10]
        with open(self.hallOfFameStoragePath, "w", encoding="utf-8") as file:
            for player_name, player_score in scores:
                file.write(f"{player_name}:{player_score}\n")


if __name__ == "__main__":
    Game(defaultTiles, tileColors, "files/tanksConfig.ini")
