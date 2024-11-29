from turtle import Turtle, setup, hideturtle, listen, update, done, tracer, onkey, ontimer, bgcolor
from freegames import floor, vector
import os
from pygame import mixer
import random
from tkinter.simpledialog import askstring
from file import File
from tank import Tank
from aiTank import AITank
from bonus import Bonus, BonusType
from tile import Tile, tileColors, defaultTiles


class Game:
    def __init__(self, initialTiles, initialTileColors, settingsFile=None):
        self.gameMode = None
        self.hallOfFameStoragePath = "files/hall_of_fame.txt"
        self.helpFilePath = "files/help.txt"
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
        self.firstTankControls = {"Up": (vector(0, 5), 0), "Down": (vector(0, -5), 180), "Left": (vector(-5, 0), 270), "Right": (vector(5, 0), 90), "Stop": "Control_R", "Shoot": "Return"}
        self.secondTankControls = {"w": (vector(0, 5), 0), "s": (vector(0, -5), 180), "a": (vector(-5, 0), 270), "d": (vector(5, 0), 90), "Stop": "Control_L", "Shoot": "Shift_L"}
        self.assignSettingsFromFile(settingsFile)
        self.tiles = list(self.initialTiles)
        self.tileColors = initialTileColors
        self.gameWidth = self.columns * self.tileSize
        self.gameHeight = self.rows * self.tileSize
        self.helpContent = File.loadFileAsArray(self.helpFilePath, "There was a problem loading help content.") if self.helpFilePath else None

        self.mapTurtle = Turtle(visible=False)
        self.messageTurtle = Turtle(visible=False)
        self.minesTurtle = Turtle(visible=False)

        self.bullets = []
        self.bonuses = []

        self.gameRunning = False
        self.gamePaused = False
        self.showingHelpFromGame = False

        self.firstTank = None
        self.secondTank = None
        self.enemyTanks = []
        self.occupiedTilesByEnemies = {}
        self.allTanks = []

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

        self.tankCentralization = self.tileSize // 10  # minimal shift of tanks to make tanks stay in the center of the title

        mixer.init()  # for playing sounds
        self.laserShootSound = mixer.Sound("files/sounds/laserShoot.wav")
        self.explosionSound = mixer.Sound("files/sounds/explosion.wav")
        self.damageSound = mixer.Sound("files/sounds/damage.wav")
        self.gameOverSound = mixer.Sound("files/sounds/game-over.mp3")

        setup(420, 420, 540, 200)
        hideturtle()
        tracer(False)

        for key in ["r", "R"]:
            onkey(self.startGame, key)
        for key in ["p", "P"]:
            onkey(self.togglePause, key)
        for key in ["h", "H"]:
            onkey(self.toggleHelpMenu, key)

        listen()
        self.startScreen()
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
            self.firstTankControls = loadedData['firstTankControls']
            self.secondTankControls = loadedData['secondTankControls']
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

    def showGameModeMenu(self):
        self.messageTurtle.clear()
        self.drawRectangle(self.messageTurtle, 0, 0, 400, 300, "white", "black", True)
        self.writeText(self.messageTurtle, 0, 100, "Select Game Mode", textFont=("Arial", 20, "bold"))
        self.writeText(self.messageTurtle, 0, 50, "Press '1' for Single Player", textFont=("Arial", 12, "normal"))
        self.writeText(self.messageTurtle, 0, 0, "Press '2' for Multiplayer", textFont=("Arial", 12, "normal"))
        self.writeText(self.messageTurtle, 0, -40, "Press 'H' for Help", textFont=("Arial", 12, "normal"))
        self.writeText(self.messageTurtle, 0, -70, "Press 'Escape' to Exit", textFont=("Arial", 12, "italic"))

        onkey(lambda: self.setGameMode("SinglePlayer"), "1")
        onkey(lambda: self.setGameMode("Multiplayer"), "2")

    def spawnBonus(self):
        if not self.gameRunning:
            return
        bonus_type = random.choice([BonusType.HEALTH, BonusType.SHOOTING_SPEED])
        possible_indexes = [index for index, value in enumerate(self.tiles) if value == Tile.ROAD.value]
        occupied_indexes = set()
        for tank in self.allTanks:
            occupied_indexes.add(self.getTileIndexFromPoint(tank.position))
        for bonus in self.bonuses:
            occupied_indexes.add(self.getTileIndexFromPoint(bonus.position))
        possible_indexes = [idx for idx in possible_indexes if idx not in occupied_indexes]
        if not possible_indexes:
            return
        random_index = random.choice(possible_indexes)
        x, y = self.getTilePosition(random_index)
        position = vector(x, y)
        bonus = Bonus(self, bonus_type, position)
        self.bonuses.append(bonus)

    def spawnBonusTimer(self):
        if not self.gameRunning:
            return
        self.spawnBonus()
        ontimer(self.spawnBonusTimer, 30000)  # Spawn a bonus every 30 seconds

    def updateBonuses(self):
        if not self.gameRunning:
            return
        for tank in self.allTanks:
            tank.updateActiveBonuses()
        ontimer(self.updateBonuses, 1000)

    def setGameMode(self, mode):
        self.gameMode = mode
        self.startGame()

    onkey(exit, "Escape")

    def saveToHallOfFame(self, name, score):
        scores = self.loadHallOfFame()

        found = False
        for i, (player_name, player_score) in enumerate(scores):
            if player_name == name:
                scores[i] = (name, max(score, player_score))
                found = True
                break

        if not found:
            scores.append((name, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        scores = scores[:10]

        with open(self.hallOfFameStoragePath, "w", encoding="utf-8") as file:
            for player_name, player_score in scores:
                file.write(f"{player_name}:{player_score}\n")

    def loadHallOfFame(self):
        if not os.path.exists(self.hallOfFameStoragePath):
            return []
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

    def showHallOfFame(self):
        scores = self.loadHallOfFame()
        self.messageTurtle.clear()
        self.drawRectangle(self.messageTurtle, 0, 0, 400, 500, "white", "black", True)
        self.writeText(self.messageTurtle, 0, 120, "🏆 Hall of Fame 🏆", textFont=("Arial", 18, "bold"))

        y_offset = 80
        for index, (name, score) in enumerate(scores):
            self.writeText(self.messageTurtle, -150, y_offset, f"{index + 1}. {name} - {score}", "left", textFont=("Arial", 12, "normal"))
            y_offset -= 30
        self.writeText(self.messageTurtle, 0, y_offset - 30, "Press 'R' to restart", textFont=("Arial", 10, "italic"))

    def getPlayerName(self):
        return askstring("Hall of Fame", "Enter your name:") or "Anonymous"

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
        possibleIndexes = [index for index, value in enumerate(self.tiles) if value == 1 and index not in occupiedIndexes]
        for _ in range(self.numberOfRandomMines):
            if not possibleIndexes:  # Break if there are no valid positions left
                break
            randomIndex = random.choice(possibleIndexes)
            self.tiles[randomIndex] = 7
            possibleIndexes.remove(randomIndex)  # Prevent duplicate selection

    def startScreen(self):
        self.gameRunning = False
        self.showGameModeMenu()
        # self.drawStartMenu()
        self.awaitStart()

    def awaitStart(self):
        onkey(self.startGame, "s")
        onkey(self.startGame, "S")
        onkey(self.toggleHelpMenu, "h")
        onkey(self.toggleHelpMenu, "H")
        onkey(exit, "Escape")

    def startGame(self):
        if self.gameRunning:  # don't start game if it's already started
            return
        setupWidth = max((self.columns + 1) * self.tileSize, 420)
        setupHeight = max((self.rows + 1) * self.tileSize, 420)

        setup(setupWidth, setupHeight, self.startGameX, self.startGameY)

        self.gameRunning = True
        self.gamePaused = False
        self.tiles = list(self.initialTiles)  # restarting map to state before changes in game
        self.drawSquare(Turtle(visible=False), -self.gameWidth, -self.gameHeight, 2 * (self.gameWidth + self.gameHeight), "black")
        self.bullets = []
        self.enemyTanks = []
        self.allTanks = []

        self.bonuses = []
        self.spawnBonus()
        self.spawnBonusTimer()
        self.updateBonuses()

        for tank in self.allTanks:
            if hasattr(tank, 'bonusDisplayTurtle'):
                tank.bonusDisplayTurtle.clear()

        firstTankPosition = self.getTilePosition(self.firstTankSpawnIndex)
        self.firstTank = Tank(self, firstTankPosition[0] + self.tankCentralization, firstTankPosition[1] + self.tankCentralization, "dark green", 0,
                              self.controls1, self.firstTankControls['Stop'], self.firstTankControls['Shoot'])
        self.allTanks = [self.firstTank]

        if self.gameMode == "Multiplayer":
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
        ontimer(self.minesTurtle.clear, self.timeAfterWhichMinesHide * 1000)
        self.roundOfMovement()

    def roundOfMovement(self):
        if not self.gameRunning or self.gamePaused:
            return
        for playerTank in list(set(self.allTanks) - set(self.enemyTanks)):
            playerTank.tankMovement()
            playerTank.moveTank()
        for enemyTank in self.enemyTanks:
            enemyTank.moveTank()
        self.processBulletsMovementsAndCollisions()
        self.checkIfGameOver()
        update()
        if self.gameRunning:
            ontimer(self.roundOfMovement, 100)

    def checkIfGameOver(self):
        if self.firstTank and self.firstTank.destroyed:
            self.endGame(self.firstTank.deathReason)
        if self.secondTank and self.secondTank.destroyed:
            self.endGame(self.secondTank.deathReason)

    @staticmethod
    def conditionalExecution(condition, function, *args, **kwargs):
        conditionResult = condition() if callable(condition) else condition
        if conditionResult:
            return function(*args, **kwargs)

    def endGame(self, reason):
        if not self.gameRunning:
            return
        self.gameRunning = False
        for tank in self.allTanks:  # draw destroyed tanks
            tank.drawTank()
        ontimer(lambda: self.conditionalExecution(not self.gameRunning and self.gameMode == "Multiplayer", self.drawModalMessage, f"Game Over!\n{reason}", "Press 'R' to restart"), 2000)
        ontimer(lambda: self.conditionalExecution(not self.gameRunning and self.gameMode != "Multiplayer", self.init_hall_of_fame), 2000)
        ontimer(lambda: self.conditionalExecution(not self.gameRunning, self.gameOverSound.play), 1000)

    def init_hall_of_fame(self):
        score = len([tank for tank in self.enemyTanks if tank.destroyed])
        player_name = self.getPlayerName()

        self.saveToHallOfFame(player_name, score)
        self.showHallOfFame()

        self.showHallOfFame()

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

    def processBulletsMovementsAndCollisions(self):
        for bullet in self.bullets[:]:
            bullet.moveBullet()
            hit = False
            tankSize = 0.8 * self.tileSize
            if bullet.position.x < -self.gameWidth // 2 or bullet.position.x > self.gameWidth // 2 or bullet.position.y < -self.gameHeight // 2 or bullet.position.y > self.gameHeight // 2:
                bullet.bulletTurtle.clear()
                self.bullets.remove(bullet)
                continue
            for tank in self.allTanks:
                if tank != bullet.shooter and tank.position.x <= bullet.position.x <= tank.position.x + tankSize and tank.position.y <= bullet.position.y <= tank.position.y + tankSize:
                    self.drawExplosion(Turtle(visible=False), bullet.position.x, bullet.position.y)
                    tank.takeDamage(bullet.shooter.attack, f"tank {tank.tankId} was shot down by tank {bullet.shooter.tankId}")
                    hit = True
            bulletTileValue = self.tiles[self.getTileIndexFromPoint(bullet.position)]
            if bulletTileValue in [Tile.INDESTRUCTIBLE_BLOCK.value, Tile.DESTRUCTIBLE_BLOCK.value]:
                if bulletTileValue == Tile.DESTRUCTIBLE_BLOCK.value:
                    self.tiles[self.getTileIndexFromPoint(bullet.position)] = Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value
                    x, y = self.getTilePosition(self.getTileIndexFromPoint(bullet.position))
                    self.drawSquare(self.mapTurtle, x, y, squareColor=self.tileColors[Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value])
                hit = True
            if hit:
                bullet.bulletTurtle.clear()
                self.bullets.remove(bullet)
                self.explosionSound.play()

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
        if not self.gamePaused:
            self.showingHelpFromGame = self.gameRunning
            self.gamePaused = True
            self.drawHelpMenu()
        else:
            self.gamePaused = False
            self.messageTurtle.clear()
            if self.showingHelpFromGame:
                self.showingHelpFromGame = False
                self.roundOfMovement()
            else:
                self.showGameModeMenu()
                self.awaitStart()

    def drawSquare(self, turtleObject, x, y, size=None, squareColor=None, circuitColor="black"):
        if not size:
            size = self.tileSize
        if circuitColor:
            turtleObject.color(circuitColor)
        else:
            turtleObject.color("")
        turtleObject.fillcolor(squareColor)
        turtleObject.up()
        turtleObject.goto(x, y)
        turtleObject.down()
        turtleObject.begin_fill()
        for count in range(4):
            turtleObject.forward(size)
            turtleObject.left(90)
        turtleObject.end_fill()

    @staticmethod
    def drawRectangle(turtleObject, x, y, rectangleWidth, rectangleHeight, fillColor="white", borderColor="black", startDrawingFromMiddle=False):
        turtleObject.color(borderColor)
        turtleObject.fillcolor(fillColor)
        turtleObject.up()
        if startDrawingFromMiddle:
            turtleObject.goto(x - rectangleWidth // 2, y - rectangleHeight // 2)
        else:
            turtleObject.goto(x, y)
        turtleObject.down()
        turtleObject.begin_fill()
        for _ in range(2):
            turtleObject.forward(rectangleWidth)
            turtleObject.left(90)
            turtleObject.forward(rectangleHeight)
            turtleObject.left(90)
        turtleObject.end_fill()
        turtleObject.up()

    @staticmethod
    def drawCircle(turtleObject, x, y, circleSize, circleColor):
        turtleObject.up()
        turtleObject.goto(x, y)
        turtleObject.dot(circleSize, circleColor)

    def drawPortal(self, turtleObject, x, y, portalSize, numberOfLayers, portalColor, backgroundColor):
        for layer in range(numberOfLayers):
            self.drawCircle(turtleObject, x, y, portalSize, portalColor)
            self.drawCircle(turtleObject, x, y, int(portalSize - 2), backgroundColor)
            portalSize = max(int(0.5 * portalSize), 4)

    @staticmethod
    def writeText(turtleObject, x, y, message, textAlign="center", textFont=("Arial", 16, "bold")):
        turtleObject.goto(x, y)
        turtleObject.write(message, align=textAlign, font=textFont)

    def drawBoard(self):
        bgcolor('black')
        for index in range(len(self.tiles)):
            tile = self.tiles[index]
            if tile > 0:
                x, y = self.getTilePosition(index)
                tileColor = self.tileColors[tile]
                self.drawSquare(self.mapTurtle, x, y, squareColor=tileColor)
                if tile == Tile.MINE.value:  # drawing mines
                    self.drawCircle(self.minesTurtle, x + self.tileSize // 2, y + self.tileSize // 2, self.tileSize // 2, "black")
                if tile == Tile.TELEPORT.value:  # drawing portals
                    self.drawPortal(self.mapTurtle, x + self.tileSize // 2, y + self.tileSize // 2, self.tileSize * 0.8, 5, "purple", "black")
        self.drawRectangle(self.mapTurtle, 0, 0, self.rows * self.tileSize, self.columns * self.tileSize, "", "white", True)  # drawing white circuit around board

    def drawExplosion(self, drawingTurtle, x, y, explosionIteration=0, maxIterations=3):
        explosionColors = ["red", "yellow", "orange"]
        explosionColor = explosionColors[explosionIteration % len(explosionColors)]
        t = self.tileSize // 20
        offsets = [(0, 0), (2 * t, 2 * t), (-2 * t, -2 * t), (-2 * t, 2 * t), (2 * t, -2 * t), (4 * t, 0), (0, 4 * t), (-4 * t, 0), (0, -4 * t)]
        for dx, dy in offsets:
            self.drawSquare(drawingTurtle, x + dx * (explosionIteration + t), y + dy * (explosionIteration + t), 2 * t + explosionIteration, explosionColor)
        if explosionIteration < maxIterations:
            ontimer(lambda: self.drawExplosion(drawingTurtle, x, y, explosionIteration + 1, maxIterations), 150)
        else:
            ontimer(drawingTurtle.clear, 200)

    def drawModalMessage(self, message, subMessage, x=0, y=0, modalWidth=350, modalHeight=120):
        self.messageTurtle.clear()
        self.drawRectangle(self.messageTurtle, x, y, modalWidth, modalHeight, "white", "black", True)
        self.writeText(self.messageTurtle, 0, 0, message)
        self.writeText(self.messageTurtle, 0, -40, subMessage, textFont=("Arial", 12, "normal"))

    def drawHelpMenu(self, modalWidth=420, modalHeight=420):
        self.messageTurtle.clear()
        self.drawRectangle(self.messageTurtle, 0, 0, modalWidth, modalHeight, "white", "black", True)
        yOffset = (modalHeight / 2) - 40
        longestTextLineWidth = 312  # I checked manually how many pixels take to write the longest line
        for line in self.helpContent:
            strippedLine = line.lstrip()
            leadingSpaces = len(line) - len(strippedLine)
            xOffset = -modalWidth / 2 + (modalWidth - longestTextLineWidth) / 2
            xOffset += leadingSpaces * 10
            self.writeText(self.messageTurtle, xOffset, yOffset, line, "left", ("Arial", 10, "normal"))
            yOffset -= 20
        if self.showingHelpFromGame:
            self.writeText(self.messageTurtle, 0, yOffset - 10, "Press 'H' to return to the game", textFont=("Arial", 8, "italic"))
        else:
            self.writeText(self.messageTurtle, 0, yOffset - 10, "Press 'H' to return to the start screen", textFont=("Arial", 8, "italic"))

    def drawStartMenu(self):
        self.messageTurtle.clear()
        modalWidth, modalHeight = 350, 250
        self.drawRectangle(self.messageTurtle, 0, 0, modalWidth, modalHeight, "white", "black", True)
        self.writeText(self.messageTurtle, 0, 70, "Tank Battle Game", textFont=("Arial", 20, "bold"))
        self.writeText(self.messageTurtle, 0, -20, "Press 'S' to Start", textFont=("Arial", 12, "normal"))
        self.writeText(self.messageTurtle, 0, -60, "Press 'H' for Help", textFont=("Arial", 12, "normal"))
        self.writeText(self.messageTurtle, 0, -100, "Press Escape for Exit", textFont=("Arial", 12, "normal"))


if __name__ == "__main__":
    Game(defaultTiles, tileColors, "files/tanksConfig.ini")
