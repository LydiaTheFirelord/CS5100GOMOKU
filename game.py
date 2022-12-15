from typing import List, Tuple, Optional

from piece import BOARD_SIZE, Piece
from agent import Agent

class Game():
    """
    Game model.
    """
    def __init__(self, agent0: Agent, agent1: Agent) -> None:
        """
        Initialize game model.\n
        agent0 plays first with black pieces.\\
        agent1 plays second with white pieces.
        """
        self.__agents = (agent0, agent1)
        self.__colors = (Piece.Black, Piece.White)
        for i in range(2):
            self.__agents[i].set_color(self.__colors[i])

        self.__running = True
        self.__step = 0
        self.__board = [[Piece.Empty for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def get_running(self) -> bool:
        """
        Get the game running status.
        """
        return self.__running

    def set_running(self, status: bool) -> None:
        """
        Set the game running status.
        """
        self.__running = status

    def get_step(self) -> int:
        """
        Get the total step.
        """
        return self.__step

    def get_board(self) -> List[List[Piece]]:
        """
        Get the current gomoku board.
        """
        return self.__board

    def check_full_board(self) -> bool:
        """
        Check if the board is running out of space.
        """
        return self.__step == BOARD_SIZE * BOARD_SIZE - 1

    def judge(self, x, y) -> Optional[Piece]:
        """
        Judge if there's a winner after place a piece at (x, y).\\
        If no winner found, return None.\n
        It's sufficient to only check around the latest piece put on the board.
        """
        DIRECTIONS = ((-1, 0), (1, 0), (-1 ,1), (1, -1), (0, 1), (0, -1), (1 ,1), (-1, -1))
        
        i = 0
        while i < len(DIRECTIONS):
            count = 1

            # Need to check both directions.
            j = 0
            while j < 2:
                next_x, next_y = x, y
                dx, dy = DIRECTIONS[i]
                for _ in range(4):
                    next_x += dx
                    next_y += dy
                    if next_x < 0 or next_x > BOARD_SIZE - 1 or next_y < 0 or next_y > BOARD_SIZE - 1:
                        break
                    if self.__board[next_x][next_y] == self.__board[x][y]:
                        count += 1
                    else:
                        break
                i += 1
                j += 1

            if count >= 5:
                return self.__board[x][y]

            i += 1

        return None

    def next_round(self) -> Tuple[int, int]:
        """
        Play the next round of the game.\\
        Caller needs to check if the game has ended or not.\n
        Return the piece position.
        """
        i = self.__step % 2
        
        x, y = self.__agents[i].move(self.__board)
        self.__board[x][y] = self.__colors[i]
        
        self.__step += 1

        return (x, y)