from chess_patterns import *
import collections
import utils
import alpha_beta_evaluation


_BLACK = 1
_WHITE = 2
_NO_COLOR = 0

_BOARD_SIZE = 15

_NEG_INF = -float('inf')
_INF = float('inf')


def _CopyBoard(chessboard):
    res = [[0 for _ in range(15)] for _ in range(15)]
    for i in range (15):
        for j in range(15):
            res[i][j] = chessboard[i][j][2]
    return res


def _CombineScoreForAi(enemy_s, my_s):
    if enemy_s.top_match_rank <= my_s.top_match_rank and enemy_s.top_match_rank <= 1:
        return _NEG_INF
    if enemy_s.top_match_rank < my_s.top_match_rank:
        rank_score_diff = (
            all_scores[enemy_s.top_match_rank] - all_scores[my_s.top_match_rank])
        return my_s.score - rank_score_diff
    if enemy_s.score > 2 * my_s.score:
        return my_s.score - enemy_s.score
    return my_s.score


def _CombineScoreForEnemy(enemy_s, ai_s):
    if ai_s.top_match_rank <= enemy_s.top_match_rank and ai_s.top_match_rank <= 1:
        return _INF
    if ai_s.top_match_rank < enemy_s.top_match_rank:
        rank_score_diff = (
            all_scores[ai_s.top_match_rank] - all_scores[enemy_s.top_match_rank])
        return enemy_s.score + rank_score_diff
    if ai_s.score > 2 * enemy_s.score:
        return ai_s.score
    return enemy_s.score


class AlphaBetaAI:
    def __init__(self, chessboard, my_color):
        self._board = _CopyBoard(chessboard)
        self._my_color = my_color
        self._enemy_color = _WHITE if my_color is _BLACK else _BLACK

        self._bestPos = (-1, -1)
        # default depth of search is 3
        self._maxDepth = 3
        # Used for printing debug info
        self.valueOfPos = collections.defaultdict(set)
        self._find_next_move_called = False

    # Wrapper for alpha beta pruning function
    def FindNextMove(self):
        assert not self._find_next_move_called
        self._find_next_move_called = True

        self._alpha_beta(self._maxDepth, alpha=_NEG_INF, beta=_INF,
                            prev_pos=None, my_turn=True)
        # print(self.valueOfPos)
        return self._bestPos

    def _alpha_beta(self, depth, alpha, beta, prev_pos, my_turn):
        if depth < self._maxDepth:
            assert prev_pos is not None
        if depth == self._maxDepth:
            assert my_turn

        if my_turn:
            return self._RunMyTurn(depth, alpha, beta, prev_pos)
        # Enemy turn.
        else:
            return self._RunEnemyTurn(depth, alpha, beta, prev_pos)

    def _RunMyTurn(self, depth, alpha, beta, prev_pos):
        """Runs AI's turn and maximizes the value."""
        search_range = utils.getSearchRange(self._board)

        enemy_raw_score = alpha_beta_evaluation.Score()
        if prev_pos is not None:
            enemy_raw_score = alpha_beta_evaluation.calculateScore(
                prev_pos[0], prev_pos[1], self._board)
        value = _NEG_INF
        for i in range(15):
            for j in range(15):
                if self._board[i][j] != _NO_COLOR or search_range[i][j] == 0:
                    continue
                if value == _NEG_INF and depth == self._maxDepth and self._bestPos == (-1, -1):
                    self._bestPos = (i, j)
                self._board[i][j] = self._my_color

                # Stop if we win.
                if alpha_beta_evaluation.IsWinMove(i, j, self._board):
                    self._board[i][j] = _NO_COLOR
                    if depth == self._maxDepth:
                        self._bestPos = (i, j)
                    return _INF

                if depth == 1:
                    my_score = alpha_beta_evaluation.calculateScore(i, j, self._board)
                    cur_move_score = _CombineScoreForAi(
                        enemy_s=enemy_raw_score, my_s=my_score)
                else:
                    cur_move_score = self._alpha_beta(
                        depth - 1, alpha, beta, (i, j), my_turn=False)
                self._board[i][j] = _NO_COLOR

                if cur_move_score > value:
                    value = cur_move_score
                    if depth == self._maxDepth:
                        self._bestPos = (i, j)
                    if value >= beta:
                        return value
                    alpha = max(alpha, value)
        return value

    def _RunEnemyTurn(self, depth, alpha, beta, prev_pos):
        """Runs enemy's turn and minimizes the value."""
        search_range = utils.getSearchRange(self._board)

        ai_raw_score = alpha_beta_evaluation.Score()
        if prev_pos is not None:
            ai_raw_score = alpha_beta_evaluation.calculateScore(
                prev_pos[0], prev_pos[1], self._board)
        value = _INF
        for i in range(15):
            for j in range(15):
                if self._board[i][j] != _NO_COLOR or search_range[i][j] == 0:
                    continue
                self._board[i][j] = self._enemy_color
                # Stop if enemy wins.
                if alpha_beta_evaluation.IsWinMove(i, j, self._board):
                    self._board[i][j] = _NO_COLOR
                    return _NEG_INF

                if depth == 1:
                    raw_score = alpha_beta_evaluation.calculateScore(i, j, self._board)
                    cur_move_score = _CombineScoreForEnemy(
                        enemy_s=raw_score, ai_s=ai_raw_score)
                else:
                    cur_move_score = self._alpha_beta(
                        depth - 1, alpha, beta, (i, j), my_turn=True)
                self._board[i][j] = _NO_COLOR

                if cur_move_score < value:
                    value = cur_move_score
                    if value <= alpha:
                        return value
                    beta = min(beta, value)
        return value
