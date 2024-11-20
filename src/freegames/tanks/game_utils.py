from freegames import floor
from constants import tankCentralization
from tiles import tiles, Tile

def offset(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    blockingTiles = [
        Tile.NO_TILE.value, Tile.RIVER.value,
        Tile.INDESTRUCTIBLE_BLOCK.value, Tile.DESTRUCTIBLE_BLOCK.value
    ]
    index = offset(point)
    if tiles[index] in blockingTiles:
        return False
    index = offset(point + 19 - tankCentralization)
    if tiles[index] in blockingTiles:
        return False
    return (point.x % 20 == tankCentralization or
            point.y % 20 == tankCentralization)
