from chess_patterns import *
import re
import collections
import utils
import evaluation


class newAI:
    def __init__(self, chessboard):
        self.chessboard = chessboard
        self.oriColor = ''
        self.usedBlack = []
        self.usedWhite = []
        self.blackPos = [[0 for _ in range(15)] for _ in range(15)]
        self.whitePos = [[0 for _ in range(15)] for _ in range(15)]
        self.occupied = [[0 for _ in range(15)] for _ in range(15)]
        self.searchRange = [[0 for _ in range(15)] for _ in range(15)]

        self.bestPos = (-1, -1)
        self.maxDepth = 4 #default depth of search is 4
        self.valueOfPos = collections.defaultdict(list) #Used for printing debug info

    # Select an algorithm by method
    def getBestPosition(self, color, alpha, beta, method):
        if method == 1:
            return self.alpha_beta(color, alpha, beta)
        if method == 2:
            return self.better_performance()



    # Initialize blackPos, whitePos, occupied according to chessboard
    def _init_black_white(self):
        for i in range(15):
            for j in range(15):
                if self.chessboard[i][j][2] == 1:
                    self.blackPos[i][j] = 1
                    self.occupied[i][j] = 1
                elif self.chessboard[i][j][2] == 2:
                    self.whitePos[i][j] = 1
                    self.occupied[i][j] = 1

    def updateChessBoard(self):
        for i in range(15):
            for j in range(15):
                if self.blackPos[i][j] == 1:
                    self.chessboard[i][j][2] = 1
                elif self.whitePos[i][j] == 1:
                    self.chessboard[i][j][2] = 2
                else:
                    self.chessboard[i][j][2] = 0

    # Wrapper for alpha beta pruning function
    def alpha_beta(self, color, alpha, beta):
        self._init_black_white()
        self.searchRange = utils.getSearchRange()
        # Depth is 4
        print("alpha beta called________________________")
        self._alpha_beta(color, self.maxDepth, alpha, beta)
        self.updateChessBoard()
        print(self.valueOfPos)
        return self.bestPos

    def _alpha_beta(self, color, depth, alpha, beta):
        if self.oriColor == '':
            self.oriColor = color
        if depth <= 0:
            if color == 1:
                i = self.usedBlack[-1][0]
                j = self.usedBlack[-1][1]
                score = evaluation.calculateScore(1, i, j, self.blackPos, self.whitePos)
            else:
                i = self.usedWhite[-1][0]
                j = self.usedWhite[-1][1]
                score = evaluation.calculateScore(2, i, j, self.blackPos, self.whitePos)
            return score
        for i in range(15):
            for j in range(15):
                # The position is not occupied and is in the range of this search
                if self.occupied[i][j] == 1 or self.searchRange[i][j] == 0:
                    continue

                self.occupied[i][j] = 1
                self.searchRange[i][j] = 0
                if color == 1:
                    self.blackPos[i][j] = 1
                    self.usedBlack.append((i, j))
                    newColor = 2
                else:
                    self.whitePos[i][j] = 1
                    self.usedWhite.append((i, j))
                    newColor = 1
                # recursion
                value = -self._alpha_beta(newColor, depth - 1, -beta, -alpha)

                if depth == 3 or depth == 4:
                    self.valueOfPos[(i, j)].append([value, depth])
                # put chess back
                self.occupied[i][j] = 0
                self.searchRange[i][j] = 1
                if color == 1:
                    self.usedBlack.remove((i, j))
                    self.blackPos[i][j] = 0
                else:
                    self.usedWhite.remove((i, j))
                    self.whitePos[i][j] = 0

                if value >= beta:
                    return beta
                if value > alpha:
                    print('update alpha', i, j, value)
                    if color == self.oriColor and depth == self.maxDepth:
                        self.bestPos = (i, j)
                    # value is the new alpha
                    alpha = value

        return alpha

    # wrapper for better performance algorithm
    def better_performance(self):
        self._init_black_white()
        self.searchRange = utils.getSearchRange()
        pos = self._better_performance()
        self.updateChessBoard()
        return pos

    def _better_performance(self):
        black_max_score = -5
        white_max_score = -5
        w_best_pos = ''
        b_best_pos = ''
        for i in range(15):
            for j in range(15):
                if self.occupied[i][j] == 0 and self.searchRange[i][j] == 1:
                    self.occupied[i][j] = 1
                    self.searchRange[i][j] = 0
                    self.whitePos[i][j] = 1

                    # Use calculateScoreBetter to do even better
                    white_score = evaluation.calculateScore(2, i, j)

                    self.whitePos[i][j] = 0
                    self.blackPos[i][j] = 1

                    black_score = evaluation.calculateScore(1, i, j)

                    self.blackPos[i][j] = 0
                    self.occupied[i][j] = 0
                    if black_score > black_max_score:
                        black_max_score = black_score
                        b_best_pos = (i, j)

                    if white_score > white_max_score:
                        white_max_score = white_score
                        w_best_pos = (i, j)

        if white_max_score > black_max_score or white_max_score >= 100000:
            return w_best_pos
        else:
            return b_best_pos
