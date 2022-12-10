from chess_patterns import *
import re


def calculateScore(color, i, j, blackPos, whitePos):
    pos_row = '2'
    pos_col = '2'
    bia_right = '2'
    bia_left = '2'
    for ii in range(15):
        if blackPos[i][ii] == 1:
            if color == 1:
                pos_row += '1'
            else:
                pos_row += '2'
        elif whitePos[i][ii] == 1:
            if color == 1:
                pos_row += '2'
            else:
                pos_row += '1'
        else:
            pos_row += '0'
    pos_row += '2'
    for ii in range(15):
        if blackPos[ii][j] == 1:
            if color == 1:
                pos_col += '1'
            else:
                pos_col += '2'
        elif whitePos[ii][j] == 1:
            if color == 1:
                pos_col += '2'
            else:
                pos_col += '1'
        else:
            pos_col += '0'
    pos_col += '2'
    # 要保存两个斜线上组成的字符串中原下棋点的位置
    bia_left_pos = -1
    bia_right_pos = -1
    bia_left_pos_rev = -1
    bia_right_pos_rev = -1
    for ii in range(max(0, i - j), min(i + (14 - j) + 1, 15)):
        if bia_right_pos == -1 and ii == i:
            bia_right_pos = ii - max(0, i - j)

            bia_right_pos_rev = min(i + (14 - j), 15) - 1 - bia_right_pos
        if blackPos[ii][ii + j - i] == 1:
            if color == 1:
                bia_right += '1'
            else:
                bia_right += '2'
        elif whitePos[ii][ii + j - i] == 1:
            if color == 1:
                bia_right += '2'
            else:
                bia_right += '1'
        else:
            bia_right += '0'
    # 加一个末边界处理 修复 bug * 4
    bia_right += '2'
    # 记得如果想用行数遍历的话，要把j当做第一个下标
    for ii in range(max(0, i - (14 - j)), min(i + j + 1, 15)):
        if bia_left_pos == -1 and ii == i:
            bia_left_pos = ii - max(0, i - (14 - j))
            bia_left_pos_rev = min(i + j + 1, 15) - 1 - bia_left_pos
        if blackPos[ii][j - (ii - i)] == 1:
            if color == 1:
                bia_left += '1'
            else:
                bia_left += '2'
        elif whitePos[ii][j - (ii - i)] == 1:
            if color == 1:
                bia_left += '2'
            else:
                bia_left += '1'
        else:
            bia_left += '0'
    bia_left += '2'
    search_flag = False
    rev_col = pos_col[::-1]
    rev_row = pos_row[::-1]
    rev_bia_left = bia_left[::-1]
    rev_bia_right = bia_right[::-1]
    score = 0
    i += 1
    j += 1
    bia_left_pos += 1
    bia_right_pos += 1
    bia_left_pos_rev += 1
    bia_right_pos_rev += 1
    for patterns in all_patterns:
        for p in patterns:
            result = re.search(p, pos_col)
            if not result or not (
                    (result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                result = re.search(p, rev_col)
            if not result or not (
                    (result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                result = re.search(p, pos_row)
            if not result or not (
                    (result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                result = re.search(p, rev_row)
            if result:
                chessRange = result.span()
                if (chessRange[0] <= i <= chessRange[1]) or (chessRange[0] <= j <= chessRange[1]):
                    score = all_scores[all_patterns.index(patterns)]
                    search_flag = True
                    break
            # 处理两种斜线上的情况
            pos = -1
            if not result or not (
                    (result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                result = re.search(p, bia_left)
                if result:
                    pos = bia_left_pos

            if not result or not result.span()[0] <= pos <= result.span()[1]:
                result = re.search(p, rev_bia_left)
                if result:
                    pos = bia_left_pos_rev

            if not result or not result.span()[0] <= pos <= result.span()[1]:
                result = re.search(p, bia_right)
                if result:
                    pos = bia_right_pos

            if not result or not result.span()[0] <= pos <= result.span()[1]:
                result = re.search(p, rev_bia_right)
                if result:
                    pos = bia_right_pos_rev

            if result:
                chessRange = result.span()
                if chessRange[0] <= pos <= chessRange[1]:
                    score = all_scores[all_patterns.index(patterns)]
                    search_flag = True
                    break
        if search_flag:
            break
    return score + board_scores[i - 1][j - 1]

def calculateScoreBetter(color, i, j, blackPos, whitePos):
        scores = []
        first_pattern = -1
        second_pattern = -1
        p_index = -1
        # 加一个初边界处理 修复 bug * 4
        pos_row = '2'
        pos_col = '2'
        bia_right = '2'
        bia_left = '2'
        for ii in range(15):
            if blackPos[i][ii] == 1:
                if color == 1:
                    pos_row += '1'
                else:
                    pos_row += '2'
            elif whitePos[i][ii] == 1:
                if color == 1:
                    pos_row += '2'
                else:
                    pos_row += '1'
            else:
                pos_row += '0'
        pos_row += '2'
        for ii in range(15):
            if blackPos[ii][j] == 1:
                if color == 1:
                    pos_col += '1'
                else:
                    pos_col += '2'
            elif whitePos[ii][j] == 1:
                if color == 1:
                    pos_col += '2'
                else:
                    pos_col += '1'
            else:
                pos_col += '0'
        pos_col += '2'
        # 要保存两个斜线上组成的字符串中原下棋点的位置
        bia_left_pos = -1
        bia_right_pos = -1
        bia_left_pos_rev = -1
        bia_right_pos_rev = -1
        # 按列数递增遍历，与按行数递增遍历一样的效果
        for ii in range(max(0, i-j), min(i+(14 - j) + 1, 15)):
            if bia_right_pos == -1 and ii == i:
                bia_right_pos = ii - max(0, i-j)  # 修复bug*2
                # print 'bia_right_pos: ' + str(bia_right_pos)
                bia_right_pos_rev = min(i+(14 - j), 15) - 1 - bia_right_pos
            if blackPos[ii][ii + j - i] == 1:
                if color == 1:
                    bia_right += '1'
                else:
                    bia_right += '2'
            elif whitePos[ii][ii + j - i] == 1:
                if color == 1:
                    bia_right += '2'
                else:
                    bia_right += '1'
            else:
                bia_right += '0'
        # 加一个末边界处理 修复 bug * 4
        bia_right += '2'
        # print 'bia_right:' + bia_right
        # 记得如果想用行数遍历的话，要把j当做第一个下标，修复bug => too long
        for ii in range(max(0, i-(14 - j)), min(i + j + 1, 15)):  # 修复 bug *2 ↑
            if bia_left_pos == -1 and ii == i:
                bia_left_pos = ii - max(0, i-(14 - j))  # 修复bug *2
                # print 'bia_left_pos: ' + str(bia_left_pos)
                bia_left_pos_rev = min(i + j + 1, 15) - 1 - bia_left_pos
            if blackPos[ii][j - (ii - i)] == 1:
                if color == 1:
                    bia_left += '1'
                else:
                    bia_left += '2'
            elif whitePos[ii][j - (ii - i)] == 1:
                if color == 1:
                    bia_left += '2'
                else:
                    bia_left += '1'
            else:
                bia_left += '0'
        bia_left += '2'
        search_flag = False
        rev_col = pos_col[::-1]
        rev_row = pos_row[::-1]
        rev_bia_left = bia_left[::-1]
        rev_bia_right = bia_right[::-1]
        score = 0

        i += 1
        j += 1
        bia_left_pos += 1
        bia_right_pos += 1
        bia_left_pos_rev += 1
        bia_right_pos_rev += 1
        for patterns in all_patterns:
            for p in patterns:
                result = re.search(p, pos_col)
                # 修复bug * 16 不等式的等于号需要加！
                if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                    result = re.search(p, rev_col)
                if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                    result = re.search(p, pos_row)
                if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                    result = re.search(p, rev_row)
                if result:
                    chessRange = result.span()
                    if (chessRange[0] <= i <= chessRange[1]) or (chessRange[0] <= j <= chessRange[1]):
                    # just to test
                    # bug * 4修复 fatal
                        score = all_scores[all_patterns.index(patterns)]
                        first_pattern = all_patterns.index(patterns)
                        scores.append(score)
                        p_index = patterns.index(p)
                        search_flag = True
                        break
                # 处理两种斜线上的情况
                pos = -1
                if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                    result = re.search(p, bia_left)
                    if result:  # bug修复 * 4
                        pos = bia_left_pos
                        # print 'test:' + str(result.span())
                        # print 'pos:' + str(pos)
                if not result or not result.span()[0] <= pos <= result.span()[1]:  # 修复bug * 3 ，pos要固定
                    result = re.search(p, rev_bia_left)
                    if result:
                        pos = bia_left_pos_rev
                        # print 'test:' + str(result.span())
                        # print 'pos:' + str(pos)
                if not result or not result.span()[0] <= pos <= result.span()[1]:
                    result = re.search(p, bia_right)
                    if result:
                        pos = bia_right_pos
                        # print 'test:' + str(result.span())
                        # print 'pos:' + str(pos)
                if not result or not result.span()[0] <= pos <= result.span()[1]:
                    result = re.search(p, rev_bia_right)
                    if result:
                        pos = bia_right_pos_rev

                if result:
                    chessRange = result.span()
                    if chessRange[0] <= pos <= chessRange[1]:
                        score = all_scores[all_patterns.index(patterns)]
                        first_pattern = all_patterns.index(patterns)
                        scores.append(score)
                        p_index = patterns.index(p)

                        search_flag = True
                        break
            if search_flag:
                break

        search_flag = False
        for patterns in all_patterns[first_pattern:]:
            for p in patterns:
                if patterns == all_patterns[first_pattern]:
                    if patterns.index(p) <= p_index:
                        continue
                result = re.search(p, pos_col)
                # 修复bug * 16 不等式的等于号需要加！
                if not result or not (
                    (result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                    result = re.search(p, rev_col)
                if not result or not (
                    (result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                    result = re.search(p, pos_row)
                if not result or not (
                    (result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                    result = re.search(p, rev_row)
                if result:
                    chessRange = result.span()
                    if (chessRange[0] <= i <= chessRange[1]) or (chessRange[0] <= j <= chessRange[1]):
                        # just to test
                        score = all_scores[all_patterns.index(patterns)]
                        # 修复bug,score列表
                        first_pattern = all_patterns.index(patterns)
                        scores.append(score)
                        p_index = patterns.index(p)
                        # print result.span()
                        search_flag = True
                        break
                # 处理两种斜线上的情况
                pos = -1
                if not result or not (
                    (result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
                    result = re.search(p, bia_left)
                    if result:  # bug修复 * 4
                        pos = bia_left_pos
                    # print 'test:' + str(result.span())
                    # print 'pos:' + str(pos)
                if not result or not result.span()[0] <= pos <= result.span()[1]:  # 修复bug * 3 ，pos要固定
                    result = re.search(p, rev_bia_left)
                    if result:
                        pos = bia_left_pos_rev
                    # print 'test:' + str(result.span())
                    # print 'pos:' + str(pos)
                if not result or not result.span()[0] <= pos <= result.span()[1]:
                    result = re.search(p, bia_right)
                    if result:
                        pos = bia_right_pos
                    # print 'test:' + str(result.span())
                    # print 'pos:' + str(pos)
                if not result or not result.span()[0] <= pos <= result.span()[1]:
                    result = re.search(p, rev_bia_right)
                    if result:
                        pos = bia_right_pos_rev
                    # print 'test:' + str(result.span())
                    # print 'pos:' + str(pos)
                if result:
                    chessRange = result.span()
                    # print search_range
                    if chessRange[0] <= pos <= chessRange[1]:
                        score = all_scores[all_patterns.index(patterns)]
                        first_pattern = all_patterns.index(patterns)
                        scores.append(score)
                        p_index = patterns.index(p)
                        # print result.span()
                        search_flag = True
                        break
            if search_flag:
                break
        # 修复bug，i-1
        # print 'origin: ' + str(Global_variables.board_scores[i - 1][j - 1]) + ' point: ' + str('%d,%d' % (i-1, j-1))
        # print 'score: ' + str(score)
        # print scores
        if len(scores) == 2:
            score = sum(scores)
        elif len(scores) != 0:
            score = max(scores)
        # print sum(scores) + Global_variables.board_scores[i-1][j-1]
        return score + board_scores[i-1][j-1]
