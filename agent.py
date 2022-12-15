from typing import List, Tuple, Optional

from piece import BOARD_SIZE, Piece

from AI import AI
from newAI import newAI
from alpha_beta_AI import AlphaBetaAI

class Agent():
    """
    Agent playing the game.\n
    It's the parent class of concrete agents.
    """
    def __init__(self) -> None:
        """
        Initialize an agent.
        """
        self.__play_first = False

    # TODO: agents should use enum Piece not int.
    def set_color(self, color: Piece) -> None:
        """
        Set the color the agent is playing.\n
        Agent with black piece plays first.
        """
        self.color = color.value
        if self.color == Piece.Black.value:
            self.__play_first = True

    # TODO: should not use parsing.
    def _parse_board(self, chessboard: List[List[Piece]]) -> List[List[List[int]]]:
        board = list()
        for i in range(BOARD_SIZE):
            row = list()
            for j in range(BOARD_SIZE):
                row.append([0, 0, chessboard[i][j].value])
            board.append(row)

        return board

    def move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        """
        Place the next piece according to the current board.\\
        The first move of an AI agent should be in the middle of the board.\n
        It should be override for human agent.
        """
        if self.__play_first:
            self.__play_first = False
            return (BOARD_SIZE // 2, BOARD_SIZE // 2)
            
        return self._normal_move(board)

    def _normal_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        """
        Place the next piece according to the current board.\n
        It should be override for AI agent and ignored for human agent.
        """
        return (-1, -1)

class AlphaBetaAgent(Agent):
    def _normal_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        chessboard = self._parse_board(board)
        ai = AI(chessboard, self.color)
        values = -100000000
        record = [-1, -1, self.color]
        # 记录values最大的那步棋下的位置
        for i in range(15):
            for j in range(15):
                # 如果该点为空，假设下在该点，修改棋盘状态
                if chessboard[i][j][2] == 0:
                    # 如果该点周围米字方向上两格都为空，就跳过该点(缩小落子范围,跳过离棋盘上其他棋子较远的点)
                    if ai.judge_empty(i, j):
                        continue
                    chessboard[i][j][2] = self.color
                    # 评估
                    evaluate = ai.ai(3 - self.color, 1, values)
                    # # 如果当前白子下法能完成五连，则将evaluate设一个较大的值
                    # if ai.judge(i, j):
                    #     evaluate = 10000000
                    #取评估值的最大值
                    if evaluate >= values:
                        values = evaluate
                        record = [i, j, self.color]
                    # 回溯
                    chessboard[i][j][2] = 0
        #print("{}:{}".format(0, values))
        #print("剪枝次数：{}".format(ai.count))
        return (record[0], record[1])

class NewAgent(Agent):
    def _normal_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        chessboard = self._parse_board(board)
        ai = newAI(chessboard)
        alpha = -100000000
        beta = 100000000
        bestPos = ai.getBestPosition(self.color, alpha, beta, 2)

        return (bestPos[0], bestPos[1])

class NewAlphaBetaAgent(Agent):
    def _normal_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        chessboard = self._parse_board(board)
        ai = AlphaBetaAI(chessboard, self.color)
        bestPos = ai.FindNextMove()

        return (bestPos[0], bestPos[1])