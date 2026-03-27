from custom import printmat

# ANSI colour codes
RED = "\x1b[31m"
RESET = "\x1b[0m"

costmat = [
    [12,23,15,40],
    [14,21,17,20],
    [13,22,20,30],
    [14,24,13,10]
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

# count zeroes in each row
for i, row in enumerate(reducedmat):
    zeroes["rows"][i] = row.count(0)

# count zeroes in each col
for j in range(size_n):
    for i in range(size_n):
        if reducedmat[i][j] == 0:
            zeroes["cols"][j] += 1

print("zero count")
print(zeroes)

# try to cover the zeroes with as few lines as possible
# as much zeroes with each line
