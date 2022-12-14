import re

# 0 represents empty, 1 represents chess, 2 represents boarder/another chess
# 100000 score (winning with 5 in a line)
pattern_5 = [re.compile(r'11111')]
# 10000 score
pattern_alive_4 = [re.compile(r'011110')]
# 8000 score
pattern_to_4 = [re.compile(r'11011'), re.compile(r'011112'), re.compile(r'10111'), re.compile(r'201111')]
# 5000 double live 3
pattern_double_alive_3 = [re.compile(r'0011100'), re.compile(r'2011100')]
# 1000
pattern_alive_sleep_3 = [re.compile(r'0011102')]
# 200
pattern_alive_3 = [re.compile(r'010110')]
# 100
pattern_double_alive_2 = [re.compile(r'001100'), re.compile(r'001102'), re.compile(r'001012')]
# 50
pattern_sleep_3 = [re.compile(r'001112'), re.compile(r'010112'), re.compile(r'011012'), re.compile(r'10011'), re.compile(r'10101'), re.compile(r'2011102')]
# 10
pattern_alive_sleep_2 = [re.compile(r'0010100'), re.compile(r'00100100')]
# 5
pattern_alive_2 = [re.compile(r'201010'), re.compile(r'2010010'),  re.compile(r'20100102'),  re.compile(r'2010102')]
# 3
pattern_sleep_2 = [re.compile(r'000112'), re.compile(r'001012'), re.compile(r'010012'), re.compile(r'10001'), re.compile(r'2010102'), re.compile(r'2011002')]
# -5 chess near the boarder
pattern_dead_4 = [re.compile(r'2\d{3}12'), re.compile(r'2\d{2}1\d{2}2')]
# -5
pattern_dead_3 = [re.compile(r'2\d{2}12')]
# -5
pattern_dead_2 = [re.compile(r'2\d12')]

all_patterns = [pattern_5, pattern_alive_4, pattern_to_4, pattern_double_alive_3, pattern_alive_sleep_3, pattern_alive_3,
                pattern_double_alive_2, pattern_sleep_3, pattern_alive_sleep_2, pattern_alive_2, pattern_sleep_2,
                pattern_dead_4, pattern_dead_3, pattern_dead_2]

all_scores = [1000000, 20000, 10000, 5000, 1000, 200, 100, 50, 10, 5, 3, -5, -5, -5]
'''
pattern_score_dict = {pattern_5: 1000000, pattern_alive_4: 10000, pattern_to_4: 5000, pattern_double_alive_3: 2000,
                      pattern_alive_sleep_3: 1000, pattern_alive_3: 500, pattern_double_alive_2: 300, pattern_sleep_3: 200,
                      pattern_alive_sleep_2: 100, pattern_alive_2: 50, pattern_sleep_2: 10, pattern_dead_4: -5, pattern_dead_3:-5,
                      pattern_dead_2: -5}
'''
board_scores = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
                [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
                [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

search_range = []
