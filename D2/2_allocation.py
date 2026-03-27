from custom import printmat

# ANSI colour codes
RED = "\x1b[31m"
RESET = "\x1b[0m"

costmat = [
    [12, 23, 15, 40],
    [14, 21, 17, 20],
    [13, 22, 20, 30],
    [14, 24, 13, 10]
]

reducedmat = costmat.copy()

# ***** reducing rows *****
for i, row in enumerate(reducedmat):
    mintime = min(row)
    for j in range(len(row)):
        reducedmat[i][j] -= mintime

print("rows reduced")
printmat(reducedmat)

# ***** reducing columns *****
for j in range(len(reducedmat[0])):
    mintime = reducedmat[0][j]
    for i in range(1, len(reducedmat)):
        if reducedmat[i][j] < mintime:
            mintime = reducedmat[i][j]

    for i in range(0, len(reducedmat)):
        reducedmat[i][j] -= mintime

print("columns reduced")
printmat(reducedmat)

# *** adding dummies ***
if len(reducedmat) < len(reducedmat[0]):
    reducedmat += [[0]*len(reducedmat[0])]
    # dummy row

elif len(reducedmat) > len(reducedmat[0]):
    for i in range(len(reducedmat)):
        reducedmat[i] += [0]
        # dummy column

size_n = len(reducedmat)  # n x n matrix


covered = {
    "rows": [False]*size_n,
    "cols": [False]*size_n
}  # if a row or col is covered

zeroes = {
    "rows": [0]*size_n,
    "cols": [0]*size_n
}  # how many zeros in a row/col

# ***** crossing the zeroes *****
while True:
    zeroes = {
    "rows": [0]*size_n,
    "cols": [0]*size_n
    }  # how many zeros in a row/col
    # reset these counts after each crossing

    # count zeroes in each row
    for i, row in enumerate(reducedmat):
        if covered["rows"][i]:
            zeroes["rows"][i] = 0
        else:
            new_zeroes = False
            for j, v in enumerate(row):
                if v == 0:
                    zeroes["rows"][i] += 1
                    if not covered["cols"][j]:
                        new_zeroes = True

            if not new_zeroes:
                zeroes["rows"][i] = 0  # no use if crossed

    # count zeroes in each col
    for j in range(size_n):
        if covered["cols"][j]:
            zeroes["cols"][j] = 0
        else:
            new_zeroes = False
            for i in range(size_n):
                if reducedmat[i][j] == 0:
                    zeroes["cols"][j] += 1
                    if not covered["rows"][i]:
                        new_zeroes = True

            if not new_zeroes:
                zeroes["cols"][j] = 0  # no use if crossed


    print("zero count")
    print(zeroes)

    all_covered = True
    # check if all zeroes are covered
    for i, row in enumerate(reducedmat):
        for j, v in enumerate(row):
            if v == 0 and \
                not (covered["cols"][j] or covered["rows"][i]):

                all_covered = False
                break  # proof by counter example
        
        if not all_covered:
            break  # receiving proof by counter example
    
    if all_covered:
        break  # already covered, move on

    # try to cover the zeroes with as few lines as possible
    # as much zeroes with each line
    max_zeroes = 0
    max_zero_line = ["", None]  # row/col, num
    for i, v in enumerate(zeroes["rows"]):
        if v > max_zeroes and not covered["rows"][i]:
            max_zeroes = v
            max_zero_line = ["rows", i]

    for i, v in enumerate(zeroes["cols"]):
        if v > max_zeroes and not covered["cols"][i]:
            max_zeroes = v
            max_zero_line = ["cols", i]

    print("crossing", max_zero_line, "\n")
    
    covered[max_zero_line[0]][max_zero_line[1]] = True


print("\nall zeroes crossed")
