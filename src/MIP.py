from pulp import LpMinimize, LpMaximize, LpProblem, LpVariable, LpInteger

from Utils import clear_console

problem = LpProblem('problem', LpMaximize)

multiplier = LpVariable('MULTIPLIER', 1, None, LpInteger)
addifier = LpVariable('ADDIFIER', 1, None, LpInteger)

players = LpVariable('PLAYERS', 2, None, LpInteger)

W = LpVariable('W', 1, None, LpInteger)
Y = LpVariable('Y', 1, None, LpInteger)
O = LpVariable('O', 1, None, LpInteger)
R = LpVariable('R', 1, None, LpInteger)
B = LpVariable('B', 1, None, LpInteger)

y = LpVariable('y', 1, None, LpInteger)
o = LpVariable('o', 1, None, LpInteger)
r = LpVariable('r', 1, None, LpInteger)

vaccine = LpVariable('vaccine', 1, None, LpInteger)
one = LpVariable('one', 1, None, LpInteger)
two = LpVariable('two', 1, None, LpInteger)
three = LpVariable('three', 1, None, LpInteger)

skip = LpVariable('skip', 1, None, LpInteger)

problem += W + Y + O + R + B + y + o + r + one + two + three + vaccine + skip, 'Deck'

problem += W + Y + O + R + B + y + o + r + one + two + three + vaccine + skip <= 100

problem += players == 2

problem += W == players
problem += B + 1 <= W

problem += Y + 1 <= y + o + r
problem += O + 1 <= o + r
problem += R + 1 <= r

problem += R + 1 <= Y

problem += Y + 1 <= y
problem += Y + O + 1 <= y + o
problem += Y + O + R + 1 <= y + o + r

problem += y + 1 <= o
problem += o + 1 <= r
problem += r <= players * 3

problem += vaccine + 1 <= one + two + three

problem += one == two + 1
problem += two == three + 1
problem += three == players - 1

problem += skip == players

problem.solve()

clear_console()

print(f'Stato della soluzione: {problem.status}\n')

print(f'W: {W.value()}')
print(f'Y: {Y.value()}')
print(f'O: {O.value()}')
print(f'R: {R.value()}')
print(f'B: {B.value()}')

print()

print(f'y: {y.value()}')
print(f'o: {o.value()}')
print(f'r: {r.value()}')

print()

print(f'vaccine: {vaccine.value()}')
print(f'+1: {one.value()}')
print(f'+2: {two.value()}')
print(f'+3: {three.value()}')

print()

print(f'skip: {skip.value()}')

print(f'')

print(f'Deck: {problem.objective.value()}')