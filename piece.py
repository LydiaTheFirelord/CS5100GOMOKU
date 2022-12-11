from enum import Enum, unique

BOARD_SIZE = 15

@unique
class Piece(Enum):
    Empty = 0
    Black = 1
    White = 2