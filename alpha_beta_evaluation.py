from chess_patterns import *
import copy
import math
import re

_BLACK = 1
_WHITE = 2
_BOARD_SIZE = 15

_CONNECT_FIVE = '11111'

def _ReverseBoardColor(board):
    for i in range(_BOARD_SIZE):
        for j in range(_BOARD_SIZE):
            if board[i][j] == _BLACK:
                board[i][j] = _WHITE
            elif board[i][j] == _WHITE:
                board[i][j] = _BLACK

def _AddBoundaryToPatternStr(s):
    """Optionally adds the boundary.

      This is needed because both the apponent color and boundary
      are represented as '2' in the string. We need to avoid adding
      boundary directly to the beginning or the end of apponent color
      otherwise that will accidentally extend its length.
    """
    res = s
    if not res.startswith('2'):
       res = '2' + res
    if not res.endswith('2'):
       res = res + '2'
    return res

def _GetDiaLeftStr(i, j, board):
    start_row = max(i - j, 0)
    col_offset = max(j - i, 0)
    res = ''
    for row in range(start_row, _BOARD_SIZE):
        col = row - start_row + col_offset
        if col >= _BOARD_SIZE:
            break
        res = res + str(board[row][col])
    return _AddBoundaryToPatternStr(res)

def _GetDiaRightStr(i, j, board):
    rev_board = copy.deepcopy(board)
    for row in range(_BOARD_SIZE):
        for col in range(0, math.ceil(_BOARD_SIZE / 2)):
            swap_pos = _BOARD_SIZE - 1 - col
            rev_board[row][col] = board[row][swap_pos]
            rev_board[row][swap_pos] = board[row][col]
    return _GetDiaLeftStr(i, _BOARD_SIZE - 1 - j, rev_board)

def _GetPatternStrScore(s):
    score = 0
    top_match_rank = 100
    for pattern_id, patterns in enumerate(all_patterns):
        for p in patterns:
            if re.search(p, s) is not None:
              score += all_scores[pattern_id]
              top_match_rank = min(pattern_id, top_match_rank)
              break
            else:
              rev_s = s[::-1]
              if re.search(p, rev_s) is not None:
                score += all_scores[pattern_id]
                top_match_rank = min(pattern_id, top_match_rank)
                break
    return score, top_match_rank


class Score:
    def __init__(self):
        self.score = 0
        self.top_match_rank = len(all_scores) - 1


def calculateScore(i, j, board):
    """Calculates the score of board for the player who just played at (i, j)"""
    local_table = copy.deepcopy(board)
    # Do the actual scoring on local_table, where the color
    # we need to score is always black.
    player_color = local_table[i][j]
    assert player_color == _BLACK or player_color == _WHITE
    if player_color == _WHITE:
        # For simplicity, we reverse the board color if the target is white so
        # that we only need to calculate score for black side.
        _ReverseBoardColor(local_table)

    row_s = ''.join([str(c) for c in local_table[i]])
    row_s = _AddBoundaryToPatternStr(row_s)

    col_s = ''.join([str(local_table[ind][j]) for ind in range(_BOARD_SIZE)])
    col_s = _AddBoundaryToPatternStr(col_s)

    dia_left = _GetDiaLeftStr(i, j, local_table)
    dia_right = _GetDiaRightStr(i, j, local_table)

    result = Score()
    result.score = board_scores[i][j]

    row_score = _GetPatternStrScore(row_s)
    result.score += row_score[0]
    result.top_match_rank = min(result.top_match_rank, row_score[1])

    col_score = _GetPatternStrScore(col_s)
    result.score += col_score[0]
    result.top_match_rank = min(result.top_match_rank, col_score[1])

    dl_score = _GetPatternStrScore(dia_left)
    result.score += dl_score[0]
    result.top_match_rank = min(result.top_match_rank, dl_score[1])

    dr_score = _GetPatternStrScore(dia_right)
    result.score += dr_score[0]
    result.top_match_rank = min(result.top_match_rank, dr_score[1])

    return result

def IsWinMove(i, j, board):
    """Checks if the player won by playing at (i, j)"""
    local_table = copy.deepcopy(board)
    # Do the actual scoring on local_table, where the color
    # we need to score is always black.
    player_color = local_table[i][j]
    assert player_color == _BLACK or player_color == _WHITE
    if player_color == _WHITE:
        # For simplicity, we reverse the board color if the target is white so
        # that we only need to calculate score for black side.
        _ReverseBoardColor(local_table)

    row_s = ''.join([str(c) for c in local_table[i]])
    if _CONNECT_FIVE in row_s:
        return True

    col_s = ''.join([str(local_table[ind][j]) for ind in range(_BOARD_SIZE)])
    if _CONNECT_FIVE in col_s:
        return True

    dia_left = _GetDiaLeftStr(i, j, local_table)
    if _CONNECT_FIVE in dia_left:
        return True
    return _CONNECT_FIVE in _GetDiaRightStr(i, j, local_table)
