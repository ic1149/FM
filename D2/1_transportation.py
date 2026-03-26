from custom import printmat

# ch1 eg 2,6,8,10,11 (same data, multiple stages)

# given
costmat = [
    [180, 110, 130, 290, 14],
    [190, 250, 150, 280, 16],
    [240, 270, 190, 120, 20],
    [11, 15, 14, 10, 50]
]

total_demand = sum(costmat[-1][:-1])
total_supply = 0
for row in costmat[:-1]:
    total_supply += row[-1]
# ***** balancing the supply and demand *****
if total_demand > total_supply:  # dummy supply
    costmat += [costmat[-1]]
    costmat[-2] = [0]*len(costmat[0])
    print("adding dummy supply")
elif total_supply > total_demand:  # dummy demand
    for row in costmat:
        row += [row[-1]]
        row[-2] = 0
    print("adding dummy demand")
else:
    print("already balanced, no dummies needed")

print("cost mat")
printmat(costmat)

# solution matrix
solmat = []
# fill in right column and bottom row from costmat
for row in costmat[:-1]:
    solmat += [[None]*(len(row)-1) + [row[-1]]]

solmat += [costmat[-1]]
# ***** Finding initial solution *****
# solution that uses all the stock 
# and meets all the demands.

# starting on top left
current_row = 0
current_col = 0
# while total demand > 0
while solmat[-1][-1] > 0:
    change = min(solmat[current_row][-1], solmat[-1][current_col])
    if solmat[current_row][current_col] is not None:
        solmat[current_row][current_col] += change
    else:
        solmat[current_row][current_col] = change

    solmat[current_row][-1] -= change  # use stock
    solmat[-1][current_col] -= change  # satisfy demand
    solmat[-1][-1] -= change  # decrease total

    if solmat[-1][current_col] == solmat[current_row][-1] == 0\
        and current_col != len(solmat[0])-1:
        # prevent degenerate solution
        # last row zero is fine

        solmat[current_row][current_col+1] = 0
        current_col += 1
        current_row += 1
    elif solmat[-1][current_col] == 0:
        current_col += 1
    else:
        current_row += 1
    print("NW method iteration")
    printmat(solmat)

print("initial solution")
printmat(solmat)


def cal_total_cost(costmat, solmat):
    total = 0

    for i in range(len(solmat)-1):
        for j in range(len(solmat[0])-1):
            if solmat[i][j] is not None:
                total += solmat[i][j] * costmat[i][j]

    return total


print("total cost: ", cal_total_cost(costmat, solmat))

# ***** Finding an improved solution *****
has_impr = True  # assume has improvement
while has_impr:
    # *** finding shadow costs ***
    shadowmat = [[None]*len(solmat[0])]

    for i in range(len(solmat)-1):
        shadowmat += [[None]]
        for j in range(len(solmat[0])-1):
            if solmat[i][j] is not None:
                shadowmat[i+1].append(costmat[i][j])
            else:
                shadowmat[i+1].append(None)
    shadowmat[1][0] = 0

    new_shadow = True
    # keep track of any changes
    # if changed, check if any new shadow costs can be filled in
    while new_shadow:
        new_shadow = False

        for i in range(1, len(solmat)):
            for j in range(1, len(solmat[0])):
                if shadowmat[i][j] is None:
                    continue

                printmat(shadowmat)
                top_shadow = shadowmat[0][j]  # dest
                left_shadow = shadowmat[i][0]  # source
                print("top,left", top_shadow, left_shadow)
                if top_shadow is not None and left_shadow is None:
                    shadowmat[i][0] = shadowmat[i][j] - top_shadow
                    new_shadow = True
                elif left_shadow is not None and top_shadow is None:
                    shadowmat[0][j] = shadowmat[i][j] - left_shadow
                    new_shadow = True
                else:
                    print("shadow costs found previously or "\
                          "panick finding shadow costs")

    print("shadow costs calculated")
    printmat(shadowmat)

    # *** finding imrovement indices ***
    imprmat = shadowmat  # improvement
    has_impr = False  # bool check if exists negative improvements
    for i in range(1, len(imprmat)):
        for j in range(1, len(imprmat[0])):
            if imprmat[i][j] is not None:
                imprmat[i][j] = None
                continue
            else:
                top_shadow = imprmat[0][j]
                left_shadow = imprmat[i][0]
                imprmat[i][j] = costmat[i-1][j-1] - top_shadow - left_shadow
                if imprmat[i][j] < 0:
                    has_impr = True

    print("improvement indices calculated")
    printmat(imprmat)

    # use the cell with the most negative improvement index
    # put theta, neighboring cells -t, diagonal that way +t
    # if all positive, optimal

    # *** stepping stone method ***
    if has_impr:
        minval = 0
        mincell = [0, 0]

        for i in range(1, len(imprmat)):
            for j in range(1, len(imprmat[0])):
                if imprmat[i][j] is None:
                    continue
                elif imprmat[i][j] < minval:
                    minval = imprmat[i][j]
                    mincell = [i-1, j-1]

        print("min cell [row, col]", mincell, "with value", minval)

        move = [0, 0]  # [row, col]
        # finding which direction's cells are filled
        if solmat[mincell[0]-1][mincell[1]] is not None:
            move[0] = -1
        else:
            move[0] = 1

        if solmat[mincell[0]][mincell[1]+1] is not None:
            move[1] = 1
        else:
            move[1] = -1

        # minimise one cell to zero, everything has to be non negative

        if solmat[mincell[0]][mincell[1]+move[1]] < \
                solmat[mincell[0]+move[0]][mincell[1]]:

            theta = solmat[mincell[0]][mincell[1]+move[1]]

            solmat[mincell[0]+move[0]][mincell[1]] -= theta
            solmat[mincell[0]][mincell[1]+move[1]] = None  # not used

        elif solmat[mincell[0]][mincell[1]+move[1]] > \
                solmat[mincell[0]+move[0]][mincell[1]]:

            theta = solmat[mincell[0]+move[0]][mincell[1]]

            solmat[mincell[0]+move[0]][mincell[1]] = None  # not used
            solmat[mincell[0]][mincell[1]+move[1]] -= theta

        else:  # same
            theta = solmat[mincell[0]+move[0]][mincell[1]]

            # both unused
            solmat[mincell[0]+move[0]][mincell[1]] = None
            solmat[mincell[0]][mincell[1]+move[1]] = None

        # diagonal in the correct direction
        solmat[mincell[0]+move[0]][mincell[1]+move[1]] += theta

        solmat[mincell[0]][mincell[1]] = theta  # enterring cell

        print("improved solution")
        print("total cost: ", cal_total_cost(costmat, solmat))
        printmat(solmat)

print("optimal solution")
print("total cost:", cal_total_cost(costmat, solmat))

# strip demand and supply row and col
# as they are not needed for output

solmat = solmat[:-1]
for i in range(len(solmat)):
    solmat[i] = solmat[i][:-1]

printmat(solmat)
