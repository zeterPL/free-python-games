from collections import deque
from tank import Tank
from utils import Vector
from tile import Tile


class AITank(Tank):
    def __init__(self, game, x, y, tankColor, tankId, target, hp=None, attack=None):
        super().__init__(game, x, y, tankColor, tankId, {}, "", "", hp, attack)
        self.target = target  # default
        self.path = []
        self.tryAppointNewPath()
        self.game.occupiedTilesByEnemies[self.tankId] = {self.game.getTileIndexFromPoint(self.position)}  # at start occupy tile where spawn
        self.stuckRounds = 0
        self.hpBeforeStuck = self.hp

    def delete(self):
        super().delete()
        self.target = None  # delete reference to other tank

    def decideTarget(self):
        potentialTargets = [tank for tank in (self.game.firstTank, self.game.secondTank) if tank and not tank.destroyed]
        if not potentialTargets:
            self.target = None
        else:
            self.target = min(potentialTargets, key=lambda target: abs(self.position - target.position))

    def isCollidingWithOtherTank(self, nextTiles):
        for otherTankId, occupiedTiles in self.game.occupiedTilesByEnemies.items():
            if otherTankId != self.tankId and not nextTiles.isdisjoint(occupiedTiles):
                return True
        return False

    def isValidPointForBot(self, point):
        return self.isValidIndexForBot(self.game.getTileIndexFromPoint(point))

    def isValidIndexForBot(self, index):
        if 0 <= index < len(self.game.tiles) and not self.isCollidingWithOtherTank({index}):
            return self.game.tiles[index] in [Tile.ROAD.value, Tile.FOREST.value, Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value]
        return False

    def findPath(self, startIndex, endIndex):
        queue = deque([(startIndex, [startIndex])])
        visited = set()
        while queue:
            current, correctPath = queue.popleft()
            if current == endIndex:
                return correctPath
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.game.getNeighbors(current, self.isValidIndexForBot):
                if neighbor not in visited:
                    queue.append((neighbor, correctPath + [neighbor]))
        return []  # No path found

    def tryAppointNewPath(self):
        if not self.target:
            return
        newPath = self.findPath(self.game.getTileIndexFromPoint(self.position), self.game.getTileIndexFromPoint(self.target.position))
        if newPath:
            self.path = newPath

    def simpleDirectionToBeCloserToTarget(self):
        dx = self.target.position.x - self.position.x
        dy = self.target.position.y - self.position.y
        movements = [
            (Vector(self.tankSpeedValue, 0), 90, dx > 0, abs(dx)),  # Move right
            (Vector(-self.tankSpeedValue, 0), 270, dx < 0, abs(dx)),  # Move left
            (Vector(0, self.tankSpeedValue), 0, dy > 0, abs(dy)),  # Move up
            (Vector(0, -self.tankSpeedValue), 180, dy < 0, abs(dy))  # Move down
        ]
        movements.sort(key=lambda m: m[3], reverse=True)
        for movementVector, direction, condition, absValue in movements:
            if condition:
                nextPosition = self.position + movementVector
                nextTiles = self.getTilesInRange(nextPosition, int(0.8 * self.game.tileSize))
                if (self.isValidPointForBot(nextPosition) and not self.isCollidingWithOtherTank(nextTiles)
                        and not self.game.tiles[self.game.getTileIndexFromPoint(self.position + 4 * movementVector)] == Tile.MINE.value):
                    self.change(movementVector, direction)
                    return
        self.change(Vector(0, 0))  # If no valid movement is found, stop the tank

    def updateDirectionPath(self):
        if not self.path:
            return self.simpleDirectionToBeCloserToTarget()
        # Get the next target position
        nextIndex = self.path[0]
        x, y = self.game.getTilePosition(nextIndex)
        nextPathTarget = Vector(x + self.game.tankCentralization, y + self.game.tankCentralization)
        if nextPathTarget.x > self.position.x:
            self.change(Vector(self.tankSpeedValue, 0), 90)
        elif nextPathTarget.x < self.position.x:
            self.change(Vector(-self.tankSpeedValue, 0), 270)
        elif nextPathTarget.y > self.position.y:
            self.change(Vector(0, self.tankSpeedValue), 0)
        elif nextPathTarget.y < self.position.y:
            self.change(Vector(0, -self.tankSpeedValue), 180)

        if self.game.getTileIndexFromPoint(self.position + self.speed) not in {self.game.getTileIndexFromPoint(self.position), nextIndex}:
            self.change(Vector(0, 0), None)
            self.tryAppointNewPath()

        if self.position == nextPathTarget:
            self.path.pop(0)  # Remove the current target from the path

    def getTilesInRange(self, point, tankRange):
        cornerOffsets = [Vector(0, 0), Vector(tankRange, 0), Vector(0, tankRange), Vector(tankRange, tankRange)]
        occupiedIndices = {self.game.getTileIndexFromPoint(point + offset) for offset in cornerOffsets}
        return occupiedIndices

    def getStuckTankOut(self):
        tileIndex = self.game.getTileIndexFromPoint(self.position)
        dx = (self.game.getTilePosition(tileIndex)[0] + self.game.tankCentralization) - self.position.x
        dy = (self.game.getTilePosition(tileIndex)[1] + self.game.tankCentralization) - self.position.y
        if dx == 0 and dy == 0:
            return  # tank is in the middle of the tile he can go itself don't need of getting it out
        elif abs(dx) > abs(dy):
            self.position.move(Vector(self.tankSpeedValue * (dx // abs(dx)), 0))
        else:
            self.position.move(Vector(0, self.tankSpeedValue * (dy // abs(dy))))
        print(f"{self.tankId=} was stuck at pos={self.position} center={self.game.getTilePosition(tileIndex)} dx={dx} dy={dy}")

    def moveTank(self, wantMove=True):
        if not self.target or self.destroyed:
            return
        if self.path:
            nextIndex = self.path[0]
            targetPosition = Vector(*self.game.getTilePosition(nextIndex)) + self.game.tankCentralization
            if self.position == targetPosition:
                self.tryAppointNewPath()
        else:
            self.tryAppointNewPath()
        self.updateDirectionPath()

        tankRange = int(0.8 * self.game.tileSize)
        currentTiles = self.getTilesInRange(self.position, tankRange)
        nextTiles = self.getTilesInRange(self.position + self.speed, tankRange)
        originalPosition = self.position  # Save original position in case the move is invalid
        wantMove = False if self.isCollidingWithOtherTank(nextTiles) else True

        self.decideToShoot()
        super().moveTank(wantMove)

        if self.position != originalPosition:
            self.game.occupiedTilesByEnemies[self.tankId] = nextTiles
            self.stuckRounds = 0
        else:
            self.game.occupiedTilesByEnemies[self.tankId] = currentTiles
            self.stuckRounds += 1
            if self.hpBeforeStuck != self.hp:
                self.hpBeforeStuck = self.hp
                self.stuckRounds = 0
            elif self.stuckRounds == 51:
                print(f"{self.tankId=} was stuck more than 50 rounds. It probably will be stuck forever.")
                self.stuckRounds = 0
            elif self.stuckRounds == 50:
                print(f"{self.tankId=} was stuck 50 rounds try teleport it to middle")
                self.teleportToMiddleTile()
            elif self.stuckRounds > 30:
                self.getStuckTankOut()
            elif self.stuckRounds == 20:
                self.shootIfNeighborTileIsDestructible()
            elif self.stuckRounds > 10:
                self.path = None
        self.decideTarget()

    def shootIfNeighborTileIsDestructible(self):
        neighbors = [
            (Vector(self.position.x + self.game.tileSize, self.position.y), 90),  # Right
            (Vector(self.position.x - self.game.tileSize, self.position.y), 270),  # Left
            (Vector(self.position.x, self.position.y + self.game.tileSize), 0),  # Up
            (Vector(self.position.x, self.position.y - self.game.tileSize), 180),  # Down
        ]
        for neighbor, direction in neighbors:
            tileIndex = self.game.getTileIndexFromPoint(neighbor)
            if 0 <= tileIndex < len(self.game.tiles) and self.game.tiles[tileIndex] == Tile.DESTRUCTIBLE_BLOCK.value:
                print(f"{self.tankId=} detected destructible block at {neighbor}. Shooting.")
                self.change(Vector(0, 0), direction)  # Turn towards the block
                self.shoot()
                return

    def decideToShoot(self):
        targetPosition = self.target.position
        if not self.loaded or not self.hasLineOfSight(targetPosition):
            return
        dx = self.target.position.x - self.position.x
        dy = self.target.position.y - self.position.y
        direction = self.direction
        if abs(dx) > abs(dy):
            if dx > 0:
                direction = 90
            elif dx < 0:
                direction = 270
        else:
            if dy > 0:
                direction = 0
            elif dy < 0:
                direction = 180
        self.change(Vector(0, 0), direction)
        self.shoot()

    def hasLineOfSight(self, targetPosition):
        centralizedBotPosition = self.position + int(self.game.tileSize * 0.4)
        rowBot, columnBot = divmod(self.game.getTileIndexFromPoint(centralizedBotPosition), self.game.columns)
        rowTarget, columnTarget = divmod(self.game.getTileIndexFromPoint(targetPosition), self.game.columns)
        if rowBot == rowTarget:  # Horizontal line of sight
            startColumn, endColumn = sorted((columnBot, columnTarget))
            tileIndices = {rowBot * self.game.columns + column for column in range(startColumn, endColumn + 1)}
            if not (targetPosition.y <= centralizedBotPosition.y <= targetPosition.y + int(self.game.tileSize * 0.8)):  # Check if target is exactly in line of shooting
                return False
        elif columnBot == columnTarget:  # Vertical line of sight
            startRow, endRow = sorted((rowBot, rowTarget))
            tileIndices = {row * self.game.columns + columnBot for row in range(startRow, endRow + 1)}
            if not (targetPosition.x <= centralizedBotPosition.x <= targetPosition.x + int(self.game.tileSize * 0.8)):  # Check if target is exactly in line of shooting
                return False
        else:
            return False
        # Check if any tile is an indestructible block
        if any(self.game.tiles[tileIndex] == Tile.INDESTRUCTIBLE_BLOCK.value for tileIndex in tileIndices):
            return False
        # Check if the tiles overlap with occupied tiles of other tanks
        return not self.isCollidingWithOtherTank(tileIndices)
