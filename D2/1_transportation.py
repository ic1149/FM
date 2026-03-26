from custom import printmat

# ch1 eg 2

# given
costmat = [
    [180, 110, 130, 290, 14],
    [190, 250, 150, 280, 16],
    [240, 270, 190, 120, 20],
    [11, 15, 14, 10, 50]
]

#solution matrix
solmat = []
# fill in right column and bottom row from costmat
for row in costmat[:-1]:
    solmat += [[0]*(len(row)-1) + [row[-1]]]

solmat += [costmat[-1]]

# starting on top left
current_row = 0
current_col = 0
# while total demand > 0
while solmat[-1][-1] > 0:
    change = min(solmat[current_row][-1], solmat[-1][current_col])
    solmat[current_row][current_col] += change
    solmat[current_row][-1] -= change  # use stock
    solmat[-1][current_col] -= change  # satisfy demand
    solmat[-1][-1] -= change  # decrease total

    if solmat[-1][current_col] == 0:
        current_col += 1
    else:
        current_row += 1

    printmat(solmat)

for i in range(len(solmat)-1):
    for j in range(len(solmat[0])-1):
        solmat[i][j] *= costmat[i][j]

total = 0

for row in solmat:
    total += sum(row)

print(total)

# ch1 eg 3
# unbalanced

# supply > demand
# add dummy demand

# m: num of rows
# n: num of cols
# degenerate: num of cells used (in feasible solution) < n+m-1

# if diagonal move, add zero
# (either way, horizontal or vertical are fine)