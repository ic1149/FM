from custom import printmat
import sys
import itertools
import copy

# ANSI colour codes
RED = "\x1b[31m"
RESET = "\x1b[0m"

# e.g. 3
costmat = [
    [9, 8, 3, 6, 10],
    [5, 5, 7, 5, 5],
    [10, 9, 3, 9, 10],
    [10, 7, 2, 9, 7],
    [9, 8, 2, 7, 10]
]

reducedmat = copy.deepcopy(costmat)

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
solution = [None]*size_n  # who does what


def count_zeroes(check_cover=True):
    zeroes = {
        "rows": [0]*size_n,
        "cols": [0]*size_n
    }  # how many zeros in a row/col
    # reset these counts after each crossing

    # count zeroes in each row
    for i, row in enumerate(reducedmat):
        if covered["rows"][i] and check_cover:
            zeroes["rows"][i] = 0
        else:
            new_zeroes = False
            for j, v in enumerate(row):
                if v == 0:
                    zeroes["rows"][i] += 1
                    if not covered["cols"][j] and check_cover:
                        new_zeroes = True

            if not new_zeroes and check_cover:
                zeroes["rows"][i] = 0  # no use if crossed

    # count zeroes in each col
    for j in range(size_n):
        if covered["cols"][j] and check_cover:
            zeroes["cols"][j] = 0
        else:
            new_zeroes = False
            for i in range(size_n):
                if reducedmat[i][j] == 0:
                    zeroes["cols"][j] += 1
                    if not covered["rows"][i] and check_cover:
                        new_zeroes = True

            if not new_zeroes and check_cover:
                zeroes["cols"][j] = 0  # no use if crossed

    return zeroes


while True:  # iteration until optimal
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
        zeroes = count_zeroes()

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
    num_crossings = (covered["cols"] + covered["rows"]).count(True)
    if num_crossings >= size_n:
        break  # optimal solution

    e = sys.maxsize  # min uncovered val

    for i, row in enumerate(reducedmat):
        for j, v in enumerate(row):
            if not covered["rows"][i] and not covered["cols"][j]\
                    and v < e:

                e = v

    for i, row in enumerate(reducedmat):
        for j, v in enumerate(row):
            crossed_times = covered["cols"][j] + covered["rows"][i]
            match crossed_times:
                case 2:
                    reducedmat[i][j] += e
                case 0:
                    reducedmat[i][j] -= e

    print("augmenting the matrix by e")
    printmat(reducedmat)

print("finding the optimal solution")
print("checking single zeroes")

work_done = True
while work_done:
    work_done = False
    zeroes = count_zeroes(check_cover=False)
    printmat(reducedmat, newline=False)
    print(zeroes, "\n")
    for i, row in enumerate(reducedmat):
        if zeroes["rows"][i] != 1:
            continue  # row does not have exactly one zero

        zero_col = row.index(0)
        solution[i] = zero_col  # assign job
        print(f"worker {i} is doing job {zero_col}\n")
        reducedmat[i] = [None]*size_n  # worker used
        for job_row in range(size_n):
            reducedmat[job_row][zero_col] = None  # job done

        work_done = True
        break

    if work_done:
        continue  # count zeroes again
        # if a job has been assinged in this iteration

    for j in range(size_n):
        if zeroes["cols"][j] != 1:
            continue  # col does not have exactly one zero

        for i in range(size_n):
            if reducedmat[i][j] == 0:
                solution[i] = j  # assign job
                print(f"worker {i} is doing job {j}\n")
                reducedmat[i] = [None]*size_n  # worker used
                for job_row in range(size_n):
                    reducedmat[job_row][j] = None  # job done

                work_done = True
                break
        
        if work_done:
            break


print("exclusive workers/jobs used")
printmat(reducedmat)
print(solution)

workers_left = [i for i in range(size_n) if solution[i] is None]
jobs_left = list(set(range(size_n)) - set(solution))

print("workers left", workers_left)
print("jobs left", jobs_left)

possible_assignments = list(itertools.permutations(workers_left))

min_cost = sys.maxsize
optimal_assignments = []
for i, assignment in enumerate(possible_assignments):
    cost = 0
    for j, worker in enumerate(assignment):
        cost += reducedmat[worker][jobs_left[j]]

    if cost < min_cost:
        min_cost = cost
        optimal_assignments = [assignment]
    elif cost == min_cost:
        optimal_assignments.append(assignment)

print(f"optimal: workers {optimal_assignments} doing jobs {jobs_left}\n")

optimal_solutions = [None]*len(optimal_assignments)
for i, row in enumerate(optimal_assignments):
    optimal_solutions[i] = solution.copy()
    for j, v in enumerate(row):
        optimal_solutions[i][v] = jobs_left[j]

print("possible optimal solutions")
for v in optimal_solutions:
    print(v)

# calculate cost
# only cal once, all optimal solutions have the same cost
cost = 0
for worker, job in enumerate(optimal_solutions[0]):
    cost += costmat[worker][job]

print("cost:", cost)