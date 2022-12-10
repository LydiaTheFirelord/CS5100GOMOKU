# Shrink the range of each search to save time
def getSearchRange(occupied):
    searchRange = [[0 for _ in range(15)]for _ in range(15)]
    for i in range(15):
        for j in range(15):
            if occupied[i][j] == 1:
                for k in range(3):
                    searchRange[max(0, i - 1)][min(14, j - 1 + k)] = 1
                    searchRange[max(0, i)][min(14, j - 1 + k)] = 1
                    searchRange[min(14, i + 1)][min(14, j - 1 + k)] = 1

    for i in range(15):
        for j in range(15):
            if occupied[i][j] == 1:
                searchRange[i][j] = 0
    return searchRange
