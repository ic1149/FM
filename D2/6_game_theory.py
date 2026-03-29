import matplotlib.pyplot as plt
import numpy as np
import sympy

# finding optimal strategies for two player zero sum games
# with no stable solution
 

payoffmat = [
    [4, -2],
    [-5, 3]
]  # ch6 e.g. 9
# for player A against B

# let A play row 1 with prob p
# therefore row 2 with prob 1-p


# if B plays 1
# A expects 4p - 5(1-p) = 9p-5

# if B plays 2
# A expects -2p + 3(1-p) = 3-5p

a_expected = []

p = sympy.Symbol("p")
a_probs = [p, 1-p]

for b_strat in range(len(payoffmat[0])):
    a_expected += [0]
    for a_strat, row in enumerate(payoffmat):
        a_expected[b_strat] += row[b_strat]*a_probs[a_strat]
print(a_expected)

for b_strat, expected in enumerate(a_expected):
    x = np.linspace(0, 1, 11) # 11 points between 0 and 1
    y = np.array([expected.evalf(subs={p: v/10}) for v in range(0,11)])
    plt.plot(x, y, label=f"B plays {b_strat}")


plt.title("expected winnings for A")
plt.xlabel("p")
plt.ylabel("winnings")
plt.grid(True)
plt.legend()


solve = a_expected[0]
for v in a_expected[1:]:
    solve -= v

sol = sympy.solve(solve)[0]
print(f"player A should play row 0 with prob {sol} "\
      f"and row 1 with prob {1-sol}")

print("the value of the game for A is",
      sympy.nsimplify(a_expected[0].evalf(subs={p:sol})))

plt.show()